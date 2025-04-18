import pytest
import asyncio
import json
from types import SimpleNamespace
from brobot.ws.ws_bot_adapter import BotAdapter
from brobot.ws.manager import ConnectionManager


# Fixture pour remplacer generate_answer par un stub
@pytest.fixture(autouse=True)
def patch_generate_answer(monkeypatch):
    async def fake_generate_answer(scenario, current_chapter, messages, context):
        # on vérifie qu'on reçoit bien des dicts role/content
        assert all("role" in m and "content" in m for m in messages)
        return "réponse_bot"

    monkeypatch.setattr(
        "brobot.ws.ws_bot_adapter.generate_answer",
        fake_generate_answer,
    )


class DummySessionService:
    def __init__(self, session):
        self._session = session
        self.added = []

    async def get_complete_scenario(self, session_id):
        return self._session

    async def add_message(self, session_id, content, role):
        # Simule un DTO avec model_dump_json()
        class DummyMsg:
            def __init__(self, content, role):
                self.content = content
                self.role = role

            def model_dump_json(self):
                return json.dumps({"content": self.content, "role": self.role})

        self.added.append((session_id, content, role))
        return DummyMsg(content, role)


@pytest.mark.asyncio
async def test_answer_user_message_success(monkeypatch):
    # Prépare un "session" minimaliste
    dummy_chapter = SimpleNamespace(id=1)
    dummy_scenario = SimpleNamespace(chapters=[dummy_chapter])
    # 1 message utilisateur
    dummy_msg = SimpleNamespace(role="user", content="bonjour")
    session_obj = SimpleNamespace(scenario=dummy_scenario, messages=[dummy_msg])

    service = DummySessionService(session_obj)
    cm = ConnectionManager()
    sent_json = []
    sent_text = []
    cm.send_json = lambda sid, data: sent_json.append((sid, data))
    cm.send_text = lambda sid, msg: sent_text.append((sid, msg))

    adapter = BotAdapter(session_id=123, session_service=service, connection_manager=cm)
    await adapter.answer_user_message()

    # get_complete_scenario a renvoyé notre session
    # add_message doit avoir été appelé avec le résultat de generate_answer
    assert service.added == [(123, "réponse_bot", "assistant")]

    # on a d'abord envoyé le signal typing stop
    assert sent_json == [(123, {"type": "typing", "status": "stop"})]

    # puis le model_dump_json() du DummyMsg
    expected = json.dumps({"content": "réponse_bot", "role": "assistant"})
    assert sent_text == [(123, expected)]


@pytest.mark.asyncio
async def test_answer_user_message_errors_when_no_session():
    service = DummySessionService(None)
    cm = ConnectionManager()
    adapter = BotAdapter(session_id=1, session_service=service, connection_manager=cm)
    with pytest.raises(Exception) as excinfo:
        await adapter.answer_user_message()
    assert "Session not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_answer_user_message_errors_when_no_scenario():
    # session sans scenario
    session_obj = SimpleNamespace(scenario=None, messages=[])
    service = DummySessionService(session_obj)
    cm = ConnectionManager()
    adapter = BotAdapter(session_id=1, session_service=service, connection_manager=cm)
    with pytest.raises(Exception) as excinfo:
        await adapter.answer_user_message()
    assert "Scenario not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_answer_user_message_errors_when_no_chapters():
    # session avec scenario mais sans chapitres
    session_obj = SimpleNamespace(scenario=SimpleNamespace(chapters=[]), messages=[])
    service = DummySessionService(session_obj)
    cm = ConnectionManager()
    adapter = BotAdapter(session_id=1, session_service=service, connection_manager=cm)
    with pytest.raises(Exception) as excinfo:
        await adapter.answer_user_message()
    assert "No chapters found" in str(excinfo.value)
