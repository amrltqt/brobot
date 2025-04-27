from agents import (
    trace,
    Runner,
)
from agents.items import ResponseInputItemParam

from brobot.bot.context import ScenarioContext
from brobot.bot.agents import prepared_agent
from brobot.models import Scenario, ScenarioChapter


async def generate_answer(
    scenario: Scenario,
    current_chapter: ScenarioChapter,
    messages: list[ResponseInputItemParam],
    context: ScenarioContext,
) -> str:
    """
    Make progress on the scenario given the current scenario state
    and the session in progress
    """

    agent = prepared_agent(
        scenario=scenario,
        chapter=current_chapter,
    )

    with trace("training"):
        result = await Runner.run(starting_agent=agent, input=messages, context=context)
        return result.final_output
