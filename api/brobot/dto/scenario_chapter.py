from pydantic import BaseModel


class ScenarioChapterWithoutContentDTO(BaseModel):
    """
    DTO for scenario chapters.
    """

    id: int
    title: str
    order: int


class ScenarioChapterDTO(BaseModel):
    """
    DTO for scenario chapters.
    """

    id: int
    title: str
    content: str
    order: int
    meta: dict = {}
