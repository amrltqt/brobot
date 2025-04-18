import pytest
import asyncio
from collections import deque
from starlette.websockets import WebSocketDisconnect
from brobot.ws.manager import ConnectionManager


class DummyWebSocket:
    def __init__(self):
        self.accepted = False
        self.sent = []
        # Simule un état CONNECTED pour le heartbeat
        self.client_state = type("CS", (), {"name": "CONNECTED"})

    async def accept(self):
        self.accepted = True

    async def send_text(self, message: str):
        if message == "force_error":
            raise Exception("forced send error")
        self.sent.append(message)

    # Pour handle_session, on re-définira receive_text dans un sous-type.


class DummyWebSocketReceive(DummyWebSocket):
    def __init__(self, messages):
        super().__init__()
        # file de messages à renvoyer
        self._messages = deque(messages)

    async def receive_text(self):
        if not self._messages:
            raise WebSocketDisconnect()
        return self._messages.popleft()


@pytest.mark.asyncio
async def test_send_text_queues_when_disconnected():
    cm = ConnectionManager()
    # pas de connexion pour le session_id=1
    await cm.send_text(1, "hello")
    # le message doit être en queue
    assert list(cm.message_queues[1]) == ["hello"]


@pytest.mark.asyncio
async def test_connect_flushes_queued_messages():
    cm = ConnectionManager()
    # queue deux messages avant connect
    await cm.send_text(42, "msg1")
    await cm.send_text(42, "msg2")

    ws = DummyWebSocket()
    await cm.connect(42, ws)

    # doit avoir accepté et vidé la file
    assert ws.accepted is True
    assert ws.sent == ["msg1", "msg2"]
    assert 42 not in cm.message_queues or not cm.message_queues[42]


@pytest.mark.asyncio
async def test_disconnect_removes_connection():
    cm = ConnectionManager()
    ws = DummyWebSocket()
    await cm.connect(7, ws)
    assert 7 in cm.active_connections

    cm.disconnect(7)
    assert 7 not in cm.active_connections


@pytest.mark.asyncio
async def test_send_text_errors_are_queued(monkeypatch):
    cm = ConnectionManager()
    # crée et enregistre un faux websocket qui lève sur send_text
    ws = DummyWebSocket()
    cm.active_connections[5] = ws

    # on force une erreur interne
    await cm.send_text(5, "force_error")
    # après exception, le message doit avoir été mis en queue
    assert list(cm.message_queues[5]) == ["force_error"]


@pytest.mark.asyncio
async def test_send_json_serializes_and_uses_send_text(monkeypatch):
    cm = ConnectionManager()
    called = []

    async def fake_send_text(session_id, message):
        called.append((session_id, message))

    cm.send_text = fake_send_text  # monkey-patch
    await cm.send_json(9, {"a": 1})
    assert called == [(9, '{"a": 1}')]


@pytest.mark.asyncio
async def test_handle_session_on_connect_and_on_receive(monkeypatch):
    cm = ConnectionManager()
    # websocket qui renvoie 3 messages (dont un vide), puis déconnecte
    ws = DummyWebSocketReceive([" first ", "", "second"])

    called_connect = []
    called_receive = []

    async def on_connect(manager, session_id, websocket):
        called_connect.append((session_id, websocket))

    async def on_receive(manager, session_id, raw):
        called_receive.append((session_id, raw))

    # on doit accepter pour que handle_session boucle
    await cm.connect(100, ws)
    # lance handle_session (il ne retournera qu'après WebSocketDisconnect)
    await cm.handle_session(100, ws, on_connect=on_connect, on_receive=on_receive)

    # on_connect exécuté une fois
    assert called_connect == [(100, ws)]
    # on_receive ne doit pas être appelé pour le message vide, et sans espaces
    assert called_receive == [(100, "first"), (100, "second")]
    # après déconnexion, la connexion doit être supprimée
    assert 100 not in cm.active_connections
