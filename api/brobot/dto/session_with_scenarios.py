import datetime


from pydantic import BaseModel

from brobot.dto.scenario_with_chapter import (
    ScenarioWithChapterDTO,
)
from brobot.dto.session_messages import SessionMessageDTO


class CompletedChapterDTO(BaseModel):
    """
    DTO for completed chapters in a scenario.
    """

    chapter_id: int
    message_id: int
    completed_at: datetime.datetime


class TrainingSessionDTO(BaseModel):
    """
    Class to represent a training session with its associated scenario.
    This is used for serialization purposes.
    """

    id: int
    created_at: datetime.datetime
    scenario: ScenarioWithChapterDTO
    messages: list[SessionMessageDTO] = []
    completions: list[CompletedChapterDTO] = []
