import datetime
from pydantic import BaseModel

from brobot.dto.scenario_chapter import (
    ScenarioChapterWithoutContentDTO,
)


class ScenarioWithChapterDTO(BaseModel):
    """
    Class to represent a scenario with its associated chapters.
    This is used for serialization purposes.
    """

    id: int
    title: str
    description: str
    created_at: datetime.datetime
    chapters: list[ScenarioChapterWithoutContentDTO] = []
