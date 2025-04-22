import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, Column, JSON

from sqlalchemy import UniqueConstraint


class TrainingSession(SQLModel, table=True):
    """
    SQLModel table representing a training session.
    Each session is associated with a user and a scenario.
    There can be only one session per (user, scenario) pair.
    """

    __tablename__ = "training_session"
    __table_args__ = (
        UniqueConstraint("user_id", "scenario_id", name="unique_user_scenario"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    scenario_id: int = Field(foreign_key="scenario.id")
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    scenario: "Scenario" = Relationship(back_populates="sessions")
    messages: List["SessionMessage"] = Relationship(back_populates="session")
    completions: List["ChapterCompletion"] = Relationship(back_populates="session")


class SessionMessage(SQLModel, table=True):
    """
    SQLModel table representing a message within a conversation session.
    """

    __tablename__ = "session_message"

    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="training_session.id")
    role: str = Field(default="user")
    content: str
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    session: "TrainingSession" = Relationship(back_populates="messages")


class ScenarioChapter(SQLModel, table=True):
    """
    Base class for Chapter models.
    """

    __tablename__ = "scenario_chapter"

    id: Optional[int] = Field(default=None, primary_key=True)
    scenario_id: int = Field(foreign_key="scenario.id")
    title: str
    content: str
    order: int
    meta: Optional[dict] = Field(default={}, sa_column=Column(JSON))

    scenario: Optional["Scenario"] = Relationship(back_populates="chapters")
    completions: List["ChapterCompletion"] = Relationship(back_populates="chapter")


class Scenario(SQLModel, table=True):
    """
    SQLModel table representing a Scenario.
    Each Scenario can have multiple Chapters.
    """

    __tablename__ = "scenario"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    chapters: List["ScenarioChapter"] = Relationship(back_populates="scenario")
    sessions: List["TrainingSession"] = Relationship(back_populates="scenario")


class ChapterCompletion(SQLModel, table=True):
    __tablename__ = "chapter_completion"

    id: Optional[int] = Field(default=None, primary_key=True)

    session_id: int = Field(foreign_key="training_session.id", index=True)
    chapter_id: int = Field(foreign_key="scenario_chapter.id", index=True)
    message_id: int = Field(foreign_key="session_message.id")

    completed_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    session: "TrainingSession" = Relationship(back_populates="completions")
    chapter: "ScenarioChapter" = Relationship(back_populates="completions")
