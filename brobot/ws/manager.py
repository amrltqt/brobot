import asyncio
import json
import logging
from collections import deque
from asyncio import Lock
from typing import Any, Awaitable, Callable, Deque, Dict, Optional

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

SessionID = int
MAX_QUEUE_SIZE = 100
logger = logging.getLogger("uvicorn.error")

# Type aliases for callbacks
OnConnectCallback = Callable[
    ["ConnectionManager", SessionID, WebSocket], Awaitable[None]
]
OnReceiveCallback = Callable[["ConnectionManager", SessionID, str], Awaitable[None]]


class ConnectionManager:
    """
    Manage WebSocket connections with:
      - auto-reconnect support via client
      - message queueing
      - heartbeat pings
      - hooks for custom logic on connect and on message
    """

    def __init__(self):
        self._lock = Lock()
        self.active_connections: Dict[SessionID, WebSocket] = {}
        self.message_queues: Dict[SessionID, Deque[str]] = {}

    async def connect(
        self,
        session_id: SessionID,
        websocket: WebSocket,
    ) -> None:
        # Accept and register socket
        await websocket.accept()
        async with self._lock:
            self.active_connections[session_id] = websocket
        logger.info(f"[{session_id}] connecté")

        # Start heartbeat and flush any queued messages
        asyncio.create_task(self._heartbeat(session_id, websocket))
        await self._flush_queue(session_id)

    def disconnect(self, session_id: SessionID) -> None:
        # Remove connection (lock not strictly needed for pop)
        self.active_connections.pop(session_id, None)
        logger.info(f"[{session_id}] déconnecté")

    async def send_text(self, session_id: SessionID, message: str) -> None:
        ws = self.active_connections.get(session_id)
        if not ws:
            return self._queue_message(session_id, message)
        try:
            await ws.send_text(message)
        except WebSocketDisconnect:
            self.disconnect(session_id)
            self._queue_message(session_id, message)
        except Exception as e:
            logger.error(f"[{session_id}] send_text error: {e}")
            self._queue_message(session_id, message)

    async def send_json(self, session_id: SessionID, data: Any) -> None:
        payload = json.dumps(data)
        await self.send_text(session_id, payload)

    def _queue_message(self, session_id: SessionID, message: str) -> None:
        # Enqueue with max size to avoid unbounded memory
        q = self.message_queues.setdefault(session_id, deque(maxlen=MAX_QUEUE_SIZE))
        q.append(message)
        logger.warning(f"[{session_id}] message en queue ({len(q)}/{MAX_QUEUE_SIZE})")

    async def _flush_queue(self, session_id: SessionID) -> None:
        ws = self.active_connections.get(session_id)
        if not ws:
            return
        q = self.message_queues.get(session_id)
        if not q:
            return
        logger.info(f"[{session_id}] flush de {len(q)} message(s)")
        while q:
            try:
                await ws.send_text(q.popleft())
            except Exception as e:
                logger.error(f"[{session_id}] erreur flush: {e}")
                break

    async def _heartbeat(self, session_id: SessionID, websocket: WebSocket) -> None:
        try:
            while True:
                await asyncio.sleep(30)
                # ping implicitly by sending empty
                if websocket.client_state.name == "CONNECTED":
                    await websocket.send_text("")
        except Exception:
            # socket closed or error
            pass

    async def handle_session(
        self,
        session_id: SessionID,
        websocket: WebSocket,
        on_connect: Optional[OnConnectCallback] = None,
        on_receive: Optional[OnReceiveCallback] = None,
    ) -> None:
        """
        Combined flow:
          1. Connect and accept
          2. Optionally run on_connect hook (e.g. send history)
          3. Enter receive loop, and for each text message run on_receive hook
        """

        # Execute user hook once after connect
        if on_connect:
            try:
                await on_connect(self, session_id, websocket)
            except Exception as e:
                logger.error(f"[{session_id}] on_connect hook error: {e}")

        try:
            # Receive loop
            while True:
                raw = await websocket.receive_text()
                # ignore empty heartbeats
                if not raw.strip():
                    continue
                # Dispatch to hook in background
                if on_receive:
                    asyncio.create_task(on_receive(self, session_id, raw))
        except WebSocketDisconnect:
            self.disconnect(session_id)
        except Exception as e:
            logger.error(f"[{session_id}] receive loop error: {e}")
            self.disconnect(session_id)
