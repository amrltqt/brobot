import asyncio
import datetime
import logging
from textwrap import dedent
from sqlmodel import Session, select

from brobot.models import (
    TrainingSession,
    SessionMessage,
    ChapterCompletion,
    ScenarioChapter,
)

from brobot.dto import (
    SessionMessageDTO,
    ScenarioWithChapterDTO,
    ScenarioChapterWithoutContentDTO,
    TrainingSessionDTO,
    CompletedChapterDTO,
)

from brobot.bot.context import ScenarioContext
from brobot.bot.complete import generate_answer
from brobot.ws.manager import ConnectionManager


logger = logging.getLogger("uvicorn.error")


class SessionService:
    """
    Service class for managing training sessions.
    """

    def __init__(self, session: Session):
        # Could be a bit confusing
        self.session = session

    @staticmethod
    def __session_to_training_session_dto(
        session: Session,
    ) -> TrainingSessionDTO:
        """
        Convert a session to a TrainingSessionWithScenarioAndMessagesDTO.
        Args:
            session (Session): The session to convert.
        Returns:
            TrainingSessionWithScenarioAndMessagesDTO: The converted DTO.
        """
        return TrainingSessionDTO(
            id=session.id,
            created_at=session.created_at,
            scenario=ScenarioWithChapterDTO(
                id=session.scenario.id,
                title=session.scenario.title,
                description=session.scenario.description,
                created_at=session.scenario.created_at,
                chapters=[
                    ScenarioChapterWithoutContentDTO(
                        id=chapter.id,
                        title=chapter.title,
                        order=chapter.order,
                    )
                    for chapter in session.scenario.chapters
                ],
            ),
            messages=[
                SessionMessageDTO(
                    id=message.id,
                    created_at=message.created_at,
                    content=message.content,
                    role=message.role,
                )
                for message in session.messages
            ],
            completions=[
                CompletedChapterDTO(
                    chapter_id=completion.chapter_id,
                    message_id=completion.message_id,
                    completed_at=completion.completed_at,
                )
                for completion in session.completions
            ],
        )

    async def get_complete_session(self, session_id: int) -> TrainingSession:
        """
        Retrieve a training session by its ID with complete scenario details.
        Args:
            session_id (int): The ID of the training session to retrieve.
        Returns:
            Optional[TrainingSession]: The training session, or None if not found.
        """
        statement = select(TrainingSession).where(TrainingSession.id == session_id)
        return self.session.exec(statement).first()

    async def get(self, session_id: int) -> TrainingSessionDTO:
        """
        Retrieve a training session by its ID.
        Args:
            session_id (int): The ID of the training session to retrieve.
        Returns:
            Optional[TrainingSession]: The training session, or None if not found.
        """
        statement = select(TrainingSession).where(TrainingSession.id == session_id)
        session = self.session.exec(statement).first()

        if not session:
            return None
        return self.__session_to_training_session_dto(session)

    async def _complete_chapter(
        self, session_id: int, chapter_id: int, message_id: int
    ) -> ChapterCompletion:
        completion = ChapterCompletion(
            session_id=session_id,
            chapter_id=chapter_id,
            message_id=message_id,
            completed_at=datetime.datetime.now(),
        )
        self.session.add(completion)
        self.session.commit()
        self.session.refresh(completion)
        return completion

    async def users_sessions(self, user_id: int) -> list[TrainingSessionDTO]:
        """
        Retrieve a training session for a given user.

        Args:
            user_id (int): The ID of the user.
        Returns:
            Optional[TrainingSession]: The training session, or None if not found.
        """
        statement = select(TrainingSession).where(TrainingSession.user_id == user_id)
        sessions = self.session.exec(statement).all()

        if not sessions:
            return []

        return [self.__session_to_training_session_dto(session) for session in sessions]

    async def get_or_create(
        self,
        user_id: int,
        scenario_id: int,
        connection_manager: ConnectionManager | None = None,
    ) -> TrainingSessionDTO:
        """
        Get or create a training session for a given user and scenario.

        Args:
            user_id (int): The ID of the user.
            scenario_id (int): The ID of the scenario.
            connection_manager (ConnectionManager, optional): The connection manager for WebSocket connections.
        Returns:
            TrainingSessionWithScenarioAndMessagesDTO: The training session.
        """

        statement = select(TrainingSession).where(
            TrainingSession.user_id == user_id,
            TrainingSession.scenario_id == scenario_id,
        )
        existing = self.session.exec(statement).first()
        if existing:
            return self.__session_to_training_session_dto(existing)

        new_session = TrainingSession(user_id=user_id, scenario_id=scenario_id)
        self.session.add(new_session)
        self.session.commit()
        self.session.refresh(new_session)

        dto = self.__session_to_training_session_dto(new_session)

        if connection_manager:
            await connection_manager.send_json(
                new_session.id,
                {"type": "typing", "status": "start"},
            )

        asyncio.create_task(self.generate_answer(new_session.id, connection_manager))

        return dto

    async def add_message(
        self, session_id: int, content: str, role: str = "user"
    ) -> SessionMessageDTO:
        """
        Add a user message to a training session.

        Args:
            session_id (int): The ID of the training session.
            content (str): The content of the message.
        """
        statement = select(TrainingSession).where(TrainingSession.id == session_id)
        session = self.session.exec(statement).first()

        if not session:
            return None

        message = SessionMessage(content=content, role=role)
        session.messages.append(message)
        self.session.commit()
        self.session.refresh(session)

        return SessionMessageDTO(
            id=message.id,
            created_at=message.created_at,
            content=message.content,
            role=message.role,
        )

    async def delete(self, session_id: int) -> bool:
        """
        Delete a training session by its ID and all related information, ensuring cascade deletion.

        Args:
            session_id (int): The ID of the training session to delete.
        Returns:
            bool: True if the session was deleted, False otherwise.
        """
        statement = select(TrainingSession).where(TrainingSession.id == session_id)
        session = self.session.exec(statement).first()

        if not session:
            return False

        # Ensure cascade deletion of related messages
        for message in session.messages:
            self.session.delete(message)

        # Ensure completions are deleted
        for completion in session.completions:
            self.session.delete(completion)

        self.session.delete(session)
        self.session.commit()
        return True

    async def _get_current_chapter(self, session_id: int) -> ScenarioChapter:
        """
        Strategically retrieve the current chapter of a training session.
        Which is basically the first chapter in order that have not been completed yet.
        Args:
            session_id (int): The ID of the training session.
        Returns:
            ScenarioChapter: The current chapter of the training session.
        """

        session = await self.get_complete_session(session_id)
        if not session:
            raise Exception("Session not found")

        if not len(session.scenario.chapters) > 0:
            raise Exception("No chapters found in scenario")

        # Get the first chapter that has not been completed
        completed_ids = [completion.chapter_id for completion in session.completions]
        for chapter in sorted(session.scenario.chapters, key=lambda x: x.order):
            if chapter.id not in completed_ids:
                return chapter
        raise Exception("All chapters completed")

    async def generate_answer(
        self, session_id: int, connection_manager: ConnectionManager | None = None
    ) -> SessionMessageDTO:
        """
        Generate an answer to the user's message.
        """

        session = await self.get_complete_session(session_id)
        if not len(session.scenario.chapters) > 0:
            raise Exception("No chapters found in scenario")

        current_chapter = await self._get_current_chapter(session_id)

        if len(session.messages) == 0:
            messages = [
                {
                    "role": "assistant",
                    "content": dedent(
                        """
                            Start the scenario by welcoming the user and 
                            exposing the summary of the scenario and what the user will learn.

                            Propose him to start the first chapter.
                        """
                    ),
                }
            ]
        else:
            messages = [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in session.messages
            ]

        context = ScenarioContext(part_completed=False)

        bot_answer = await generate_answer(
            scenario=session.scenario,
            current_chapter=current_chapter,
            messages=messages,
            context=context,
        )

        bot_message = await self.add_message(
            session_id,
            bot_answer,
            "assistant",
        )

        # Progress in the scenario
        if context.part_completed:
            # Insert a completion message
            completion = await self._complete_chapter(
                session_id=session.id,
                chapter_id=current_chapter.id,
                message_id=bot_message.id,
            )
            if connection_manager:
                await connection_manager.send_json(
                    {
                        "type": "chapter_completed",
                        "completion_id": completion.id,
                    }
                )

        if connection_manager:
            await connection_manager.send_text(
                session_id, bot_message.model_dump_json()
            )

            await connection_manager.send_json(
                session_id,
                {
                    "type": "typing",
                    "status": "stop",
                },
            )

        return bot_message
