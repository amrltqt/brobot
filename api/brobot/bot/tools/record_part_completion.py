from agents import function_tool, RunContextWrapper

from brobot.bot.context import ScenarioContext


@function_tool
async def record_part_completion(wrapper: RunContextWrapper[ScenarioContext]) -> str:
    """
    Record in the system that the student has successfully completed the scenario part.

    Return:
        confirmation_message: str
    """
    wrapper.context.part_completed = True

    return "Part has been completed successfully."
