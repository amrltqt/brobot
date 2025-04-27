import datetime
from typing import Optional, List, Dict
from sqlmodel import Field, SQLModel, Relationship, JSON

from sqlalchemy import UniqueConstraint, Column, Integer, String, DateTime, Boolean


def now_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: int = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    name: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime, nullable=False),
        default_factory=now_utc,
    )

    hashed_password: str = Field(sa_column=Column(String(255), nullable=False))
    is_active: bool = Field(
        default=True, sa_column=Column(Boolean, nullable=False, default=True)
    )
    is_superuser: bool = Field(
        default=False, sa_column=Column(Boolean, nullable=False, default=False)
    )

    sessions: List["TrainingSession"] = Relationship(back_populates="user")


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

    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    user_id: int = Field(foreign_key="user.id")
    scenario_id: int = Field(foreign_key="scenario.id")
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime, nullable=False),
        default_factory=now_utc,
    )

    user: "User" = Relationship(back_populates="sessions")
    scenario: "Scenario" = Relationship(back_populates="sessions")
    messages: List["SessionMessage"] = Relationship(back_populates="session")
    completions: List["ChapterCompletion"] = Relationship(back_populates="session")


class SessionMessage(SQLModel, table=True):
    """
    SQLModel table representing a message within a conversation session.
    """

    __tablename__ = "session_message"

    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    session_id: int = Field(foreign_key="training_session.id")
    role: str = Field(sa_column=Column(String(50), nullable=False, default="user"))
    content: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime, nullable=False),
        default_factory=now_utc,
    )

    session: "TrainingSession" = Relationship(back_populates="messages")


class ScenarioChapter(SQLModel, table=True):
    """
    Base class for Chapter models.
    """

    __tablename__ = "scenario_chapter"

    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    scenario_id: int = Field(foreign_key="scenario.id", nullable=False)
    title: str = Field(sa_column=Column(String(255), nullable=False))
    content: str = Field(sa_column=Column(String, nullable=False))
    order: int = Field(sa_column=Column(Integer, nullable=False))

    meta: Optional[Dict] = Field(default_factory=dict, sa_column=Column(JSON))

    scenario: Optional["Scenario"] = Relationship(back_populates="chapters")
    completions: List["ChapterCompletion"] = Relationship(back_populates="chapter")


class Scenario(SQLModel, table=True):
    """
    SQLModel table representing a Scenario.
    Each Scenario can have multiple Chapters.
    """

    __tablename__ = "scenario"

    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))
    title: str = Field(sa_column=Column(String(255), nullable=False))
    slug: str = Field(sa_column=Column(String(255), nullable=False, unique=True))
    description: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime, nullable=False),
        default_factory=now_utc,
    )

    chapters: List["ScenarioChapter"] = Relationship(back_populates="scenario")
    sessions: List["TrainingSession"] = Relationship(back_populates="scenario")


class ChapterCompletion(SQLModel, table=True):
    __tablename__ = "chapter_completion"

    id: int = Field(sa_column=Column(Integer, primary_key=True, autoincrement=True))

    session_id: int = Field(foreign_key="training_session.id", index=True)
    chapter_id: int = Field(foreign_key="scenario_chapter.id", index=True)
    message_id: int = Field(foreign_key="session_message.id")

    completed_at: datetime.datetime = Field(
        sa_column=Column(DateTime, nullable=False),
        default_factory=now_utc,
    )

    session: "TrainingSession" = Relationship(back_populates="completions")
    chapter: "ScenarioChapter" = Relationship(back_populates="completions")
