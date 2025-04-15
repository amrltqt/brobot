from typing import List

from fastapi import APIRouter, HTTPException, Depends, status

from sqlmodel import Session

from brobot.database import get_session

from brobot.dto import TrainingSessionWithScenarioAndMessagesDTO

from brobot.services.session import SessionService

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
    print(sessions)

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
