from pydantic import BaseModel


class CreateScenarioChapterDTO(BaseModel):
    """
    DTO for creating a scenario chapter.
    """

    title: str
    content: str
    order: int
    meta: dict = {}


class CreateScenarioDTO(BaseModel):
    """
    DTO for creating a scenario.
    """

    slug: str
    title: str
    description: str
    chapters: list[CreateScenarioChapterDTO]
