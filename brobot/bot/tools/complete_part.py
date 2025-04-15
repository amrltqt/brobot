from agents import function_tool, RunContextWrapper

from brobot.bot.context import ScenarioContext


@function_tool
async def complete_part(wrapper: RunContextWrapper[ScenarioContext]) -> str:
    """
    Record in the system that the student have successfully completed the scenario part.

    Return:
        confirmation_message: str
    """
    wrapper.context.part_completed = True

    return "Part have been completed"
