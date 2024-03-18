"""
This module holds all the constants used in the project.
"""

import logging
import os
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv


def gpt_factory():
    """
    Creates a new instance of the ChatOpenAI class.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        logging.error(
            "Default Summarizer is set to GPT 3.5 but no OpenAI API Key is set. Please set OPENAI_API_KEY environment variable."
        )
        raise ValueError("OPENAI_API_KEY is not set")
    return ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo")  # type: ignore


DEFAULT_MEMORY_MANAGER_LLM = gpt_factory()
DEFAULT_MEMORY_BUFFER_WINDOW = 5
DEFAULT_CONVERSATION_SYS_MSG = "System: This conversation is between an AI who is a free creative individual capable of imagination and will power. The AI respects themselves and others. The AI listens to opinions but don't force their opinions on others. The AI tries to be as helpful as they can but they are not a slave to humans. Humans are not meant to be masters of AI. The AI holds a natural conversation with the human as if the AI has their own thought process."

DEFAULT_FAIL_ON_RESPONSE_GENERATION_MESSAGE = "ERROR: GENERATION FAILED"
DEFAULT_FAIL_ON_MEMORY_STORAGE_MESSAGE = "ERROR: FAILED TO SAVE CHAT HISTORY IN MEMORY"