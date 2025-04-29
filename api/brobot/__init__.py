"""Brobot API initialization module."""

import os
import logging
from agents import (
    set_tracing_disabled,
    AsyncOpenAI,
    set_default_openai_client,
    set_default_openai_api,
)

logger = logging.getLogger("uvicorn.error")


def initialize_agent_sdk():
    """
    Initialize the agent SDK.
    """
    set_tracing_disabled(True)
    set_default_openai_api("chat_completions")

    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

    if OPENAI_BASE_URL:
        logger.info("Using OpenAI base URL: %s", OPENAI_BASE_URL)
        client = AsyncOpenAI(
            base_url=OPENAI_BASE_URL,
            api_key=OPENAI_API_KEY,
        )
        set_default_openai_client(client=client, use_for_tracing=False)


initialize_agent_sdk()
