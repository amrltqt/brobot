import json
import asyncio
import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, WebSocket
from sqlmodel import Session

from brobot.database import get_session
from brobot.dto import TrainingSessionWithScenarioAndMessagesDTO
from brobot.services.session import SessionService
from brobot.ws.manager import ConnectionManager
from brobot.ws.ws_bot_adapter import BotAdapter


router = APIRouter()


# Global instance of ConnectionManager to handle sessions
connection_manager = ConnectionManager()


logger = logging.getLogger("uvicorn.error")

router = APIRouter()

USER_ID = 1  # Placeholder for user ID, should be replaced with actual user ID from authentication


@router.get("/{session_id}", response_model=TrainingSessionWithScenarioAndMessagesDTO)
async def api_get_training_session(session_id: int, db: Session = Depends(get_session)):
    """
    Retrieve a training session and all its associated messages.
    """
    sevice = SessionService(db)
    session = await sevice.get(session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/", response_model=List[TrainingSessionWithScenarioAndMessagesDTO])
async def api_my_training_sessions(db: Session = Depends(get_session)):
    """
    Retrieve all training sessions from the database.
    """
    service = SessionService(db)
    sessions = await service.users_sessions(USER_ID)

    return sessions


@router.post("/{scenario_id}", status_code=status.HTTP_201_CREATED)
async def api_create_training_session(
    scenario_id: int, db: Session = Depends(get_session)
):
    """
    Create a new training session for a given scenario.
    """
    service = SessionService(db)
    session = await service.get_or_create(USER_ID, scenario_id)
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_training_session(
    session_id: int, db: Session = Depends(get_session)
):
    """
    Delete a training session by its ID.
    """
    service = SessionService(db)
    success = await service.delete(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")


@router.websocket("/ws/{session_id}")
async def session_ws(
    websocket: WebSocket, session_id: int, db: Session = Depends(get_session)
):
    await connection_manager.connect(session_id, websocket)

    service = SessionService(db)

    async def send_history(cm: ConnectionManager, sid: int, ws: WebSocket):
        session = await service.get(sid)
        logger.info("Sending history to client", extra={"session_id": sid})
        for msg in session.messages:
            await cm.send_text(sid, msg.model_dump_json())

    async def handle_incoming(cm: ConnectionManager, sid: int, raw: str):
        if not raw:
            logger.warning(f"[{sid}] Received empty message")
            return

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            logger.error(f"[{sid}] Invalid JSON: {raw}")
            return

        await cm.send_json(sid, {"type": "typing", "status": "start"})

        user_message = await service.add_message(
            sid,
            data.get("content"),
            data.get("role"),
        )

        await cm.send_text(sid, user_message.model_dump_json())

        adapter = BotAdapter(
            session_id=sid,
            session_service=service,
            connection_manager=cm,
        )
        asyncio.create_task(adapter.answer_user_message())

    await connection_manager.handle_session(
        session_id,
        websocket,
        on_connect=send_history,
        on_receive=handle_incoming,
    )
