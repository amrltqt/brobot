import json
import asyncio
import logging

from typing import Dict, List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlmodel import Session

from brobot.database import get_session

from brobot.services.session import SessionService

from brobot.bot.complete import generate_answer
from brobot.bot.context import ScenarioContext

router = APIRouter()
logger = logging.getLogger("uvicorn.error")


class ConnectionManager:
    """
    This manager handles WebSocket connections by session (one client per session).
    It allows:
      - Accepting a new connection and sending queued messages.
      - Sending a message to the connected client.
      - Temporarily storing messages for a disconnected client.
    """

    def __init__(self):
        # For each session_id, store the single connected websocket (if any)
        self.active_connections: Dict[int, WebSocket] = {}
        # Queue for each session to store messages that couldn't be delivered immediately
        self.message_queues: Dict[int, List[str]] = {}

    async def connect(self, session_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"Client connected for session {session_id}.")
        # If there are queued messages from previous disconnections, send them now
        if session_id in self.message_queues and self.message_queues[session_id]:
            logger.info(
                f"Sending {len(self.message_queues[session_id])} queued message(s) for session {session_id}."
            )
            for message in self.message_queues[session_id]:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error while sending a queued message: {str(e)}")
            self.message_queues[session_id] = []

    def disconnect(self, session_id: int):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"Client disconnected from session {session_id}.")

    async def send_personal_message(self, session_id: int, message: str):
        websocket = self.active_connections.get(session_id)
        if websocket:
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error while sending personal message: {str(e)}")
                self.queue_message(session_id, message)
        else:
            self.queue_message(session_id, message)

    async def defer_message_generation(self, session_id: int, db: Session):
        """
        This method is called to defer message generation for a session.
        It can be used to manage the flow of messages based on certain conditions.
        """
        # Placeholder for future implementation
        logger.info(f"Message generation deferred for session {session_id}.")

        session_service = SessionService(db)

        training_session = await session_service.get_complete_scenario(session_id)
        scenario = training_session.scenario
        messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in sorted(training_session.messages, key=lambda x: x.created_at)
        ]
        context = ScenarioContext(part_completed=False)

        answer = await generate_answer(
            scenario=scenario,
            current_chapter=scenario.chapters[0],
            messages=messages,
            context=context,
        )

        message = await session_service.add_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )
        await self.send_message(
            session_id=session_id,
            message=message.model_dump_json(),
        )

    def queue_message(self, session_id: int, message: str):
        if session_id not in self.message_queues:
            self.message_queues[session_id] = []
        self.message_queues[session_id].append(message)
        logger.info(f"No active connection for session {session_id}. Message queued.")

    async def send_message(self, session_id: int, message: str):
        await self.send_personal_message(session_id, message)


# Global instance of ConnectionManager to handle sessions
connection_manager = ConnectionManager()


@router.websocket("/{session_id}")
async def session_ws(
    websocket: WebSocket, session_id: int, db: Session = Depends(get_session)
):
    """
    WebSocket endpoint to handle messages for a session.
    - On connection, a welcome message is sent.
    - Received messages are parsed and, if le rôle est "user" ou "assistant", sont sauvegardés en base de données.
    - Other messages (par exemple, de type "log") ne sont enregistrés qu'à titre informatif.
    - On disconnection, the event is logged.
    """

    service = SessionService(db)

    # Ensure session_id is an integer
    session_id = int(session_id)

    # Accept the connection
    await connection_manager.connect(session_id, websocket)

    # Send an acknowledgment to the client.
    await connection_manager.send_message(
        session_id,
        json.dumps({"role": "log", "content": "WebSocket connection established"}),
    )

    session = await service.get(session_id)

    for message in session.messages:
        await connection_manager.send_message(
            session_id=session_id, message=message.model_dump_json()
        )

    try:
        while True:
            content = await websocket.receive_text()
            logger.info(f"Message received in session {session_id}: {content}")

            message = await service.add_message(session_id, content)
            logger.info(f"Message saved in DB for session {session_id}.")

            await connection_manager.send_message(
                session_id=session_id, message=message.model_dump_json()
            )

            asyncio.create_task(
                connection_manager.defer_message_generation(
                    session_id,
                    db,
                )
            )

    except WebSocketDisconnect:
        connection_manager.disconnect(session_id)
        logger.info(f"Client disconnected from session {session_id}.")
    except Exception as e:
        logger.error(f"Error handling session {session_id}: {str(e)}")
        connection_manager.disconnect(session_id)
