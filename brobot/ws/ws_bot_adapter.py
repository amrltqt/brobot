import logging
from brobot.bot.complete import generate_answer
from brobot.bot.context import ScenarioContext
from brobot.dto import (
    ScenarioChapterDTO,
    TrainingSessionWithScenarioAndMessagesDTO,
    SessionMessageDTO,
)
from brobot.services.session import SessionService
from brobot.ws.manager import ConnectionManager

logger = logging.getLogger("uvicorn.error")


class BotAdapter:
    def __init__(
        self,
        session_id: int,
        session_service: SessionService,
        connection_manager: ConnectionManager,
    ):
        self.session_id = session_id
        self.connection_manager = connection_manager
        self.session_service = session_service

    async def _get_session(self):
        """
        Retrieve the session from the session service.
        """
        session = await self.session_service.get_complete_scenario(self.session_id)
        if not session:
            logger.error(f"Session {self.session_id} not found.")
            raise Exception("Session not found")
        return session

    async def _identify_current_chapter(
        self, session: TrainingSessionWithScenarioAndMessagesDTO
    ) -> ScenarioChapterDTO:
        """
        Identify the current chapter based on the session's messages.
        """
        if not session.scenario:
            logger.error("Session has no scenario.")
            raise Exception("Scenario not found")

        if not session.scenario.chapters:
            logger.error("Scenario has no chapters.")
            raise Exception("No chapters found")

        # Let's stub to the first chapter
        if not len(session.scenario.chapters) > 0:
            logger.error("No chapters found in scenario.")
            raise Exception("No chapters found in scenario")

        current_chapter = session.scenario.chapters[0]
        return current_chapter

    def _convert_message(self, messages: list[SessionMessageDTO]):
        """
        Convert messages to the format required by the bot.
        """
        return [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in messages
        ]

    async def answer_user_message(self):
        """
        Generate an answer to the user's message.
        """

        session = await self._get_session()
        current_chapter = await self._identify_current_chapter(session)
        messages = self._convert_message(session.messages)
        context = ScenarioContext(part_completed=False)

        bot_answer = await generate_answer(
            scenario=session.scenario,
            current_chapter=current_chapter,
            messages=messages,
            context=context,
        )

        if bot_answer:
            bot_message = await self.session_service.add_message(
                self.session_id,
                bot_answer,
                "assistant",
            )

            # Stop typing signal
            res = self.connection_manager.send_json(
                self.session_id, {"type": "typing", "status": "stop"}
            )
            try:
                await res
            except TypeError:
                # stub synchrones peuvent retourner None
                pass

            # Envoi du message du bot
            res = self.connection_manager.send_text(
                self.session_id, bot_message.model_dump_json()
            )
            try:
                await res
            except TypeError:
                pass
