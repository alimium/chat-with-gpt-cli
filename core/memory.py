"""
This module defines the ConversationMemory and MemoryManager classes for managing conversation memories.

Classes:
- ConversationMemory: A class representing the conversation memory.
- MemoryManager: The MemoryManager class manages conversation memories for different memory keys.
"""

from enum import Enum
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.llms.base import BaseLanguageModel

from .constants import DEFAULT_MEMORY_BUFFER_WINDOW, DEFAULT_MEMORY_MANAGER_LLM


class MessageRoles(Enum):
    """
    An enumeration representing the roles of messages in a conversation.
    """

    HUMAN = "Human"
    AI = "AI"


class ConversationMemory:
    """
    A class representing the conversation memory.

    Attributes:
        _chat_history (ConversationBufferWindowMemory): The conversation buffer window memory.
        _chat_summary (ConversationSummaryMemory): The conversation summary memory.
    """

    def __init__(self, llm: BaseLanguageModel, k: int) -> None:
        """
        Initializes a new instance of the ConversationMemory class.

        Args:
            llm (BaseLanguageModel): The base language model.
            k (int): The size of the conversation buffer window.
        """
        self._chat_history = ConversationBufferWindowMemory(
            k=k, memory_key="conversation_history"
        )
        self._chat_summary = ConversationSummaryMemory(
            llm=llm, memory_key="conversation_summary"
        )

    def get_chat_history(self) -> str:
        """
        Retrieves the conversation history.

        Returns:
            str: The conversation history.
        """
        return self._chat_history.load_memory_variables({})["conversation_history"]

    def get_chat_summary(self) -> str:
        """
        Retrieves the conversation summary.

        Returns:
            str: The conversation summary.
        """
        return self._chat_summary.load_memory_variables({})["conversation_summary"]

    def clear_chat_history(self):
        """
        Clears the conversation history.
        """
        self._chat_history.clear()

    def clear_chat_summary(self):
        """
        Clears the conversation summary.
        """
        self._chat_summary.clear()

    def clear_from_chat_history(self, n: int):
        """
        Clears the specified number of messages from the conversation history.

        Args:
            n (int): The number of messages to clear.
        """
        raise NotImplementedError("Coming soon...")

    def insert_ai_message(self, message: str):
        """
        Inserts an AI message into the conversation history.

        Args:
            message (str): The AI message to insert.
        """
        self._chat_history.chat_memory.add_ai_message(message)

    def insert_user_message(self, message: str):
        """
        Inserts a user message into the conversation history.

        Args:
            message (str): The user message to insert.
        """
        self._chat_history.chat_memory.add_user_message(message)

    def insert_to_chat_history(self, index: int, role: str, message: str):
        """
        Inserts a message into the conversation history at the specified index.

        Args:
            index (int): The index at which to insert the message.
            role (str): The role of the message (e.g., "AI" or "User").
            message (str): The message to insert.
        """
        raise NotImplementedError("Coming soon...")

    def update_chat_summary(self):
        """
        Updates the conversation summary.
        """
        existing_summary = self.get_chat_summary()
        messages = self._chat_history.chat_memory.messages
        new_summary = self._chat_summary.predict_new_summary(messages, existing_summary)
        self._chat_summary.buffer = new_summary

    def __len__(self) -> int:
        """
        Returns the number of messages in the conversation history.

        Returns:
            int: The number of messages in the conversation history.
        """
        return len(self._chat_history.chat_memory.messages)

    def __str__(self, key=str | None) -> str:
        """
        Returns a string representation of the conversation memory.

        Args:
            key (str | None): The key to specify which part of the conversation memory to return.
                Possible values are "history", "summary", or None (default).

        Returns:
            str: The string representation of the conversation memory.
        """
        if key == "history":
            return f"Conversation History:\n{self.get_chat_history()}"
        elif key == "summary":
            return f"Conversation Summary:\n{self.get_chat_summary()}"
        else:
            return f"""Conversation Summary:\n{self.get_chat_summary()}
            
            Conversation History:\n{self.get_chat_history()}"""

    def __dict__(self) -> dict:
        """
        Returns a dictionary representation of the conversation memory.

        Returns:
            dict: The dictionary representation of the conversation memory.
        """
        return {"history": self.get_chat_history(), "summary": self.get_chat_summary()}


class MemoryManager:
    """
    The MemoryManager class manages conversation memories for different memory keys.

    Args:
        llm (BaseLanguageModel, optional): The language model to use for conversation memories.
            Defaults to DEFAULT_MEMORY_MANAGER_LLM.
        k (int, optional): The buffer window size for conversation memories.
            Defaults to DEFAULT_MEMORY_BUFFER_WINDOW.
    """

    class MessageRoles(Enum):
        """
        An enumeration representing the roles of messages in a conversation.
        """

        HUMAN = "User"
        AI = "AI"

    def __init__(
        self,
        llm: BaseLanguageModel = DEFAULT_MEMORY_MANAGER_LLM,
        k: int = DEFAULT_MEMORY_BUFFER_WINDOW,
    ) -> None:
        """
        Initialize a MemoryManager object.

        Args:
            llm (BaseLanguageModel, optional): The language model to use for conversation memories.
                Defaults to DEFAULT_MEMORY_MANAGER_LLM.
            k (int, optional): The buffer window size for conversation memories.
                Defaults to DEFAULT_MEMORY_BUFFER_WINDOW.
        """
        self._llm = llm
        self._k = k
        self._memory_bank: dict[str, ConversationMemory] = {}

    def get_memory(self, memory_key: str) -> ConversationMemory:
        """
        Get the conversation memory for the specified memory key.

        If the memory key does not exist, a new conversation memory is created and stored.

        Args:
            memory_key (str): The key to identify the conversation memory.

        Returns:
            ConversationMemory: The conversation memory associated with the memory key.
        """
        if memory_key not in self._memory_bank:
            self._memory_bank[memory_key] = ConversationMemory(llm=self._llm, k=self._k)
        return self._memory_bank[memory_key]

    def get_chat_history(self, memory_key: str) -> str | None:
        """
        Get the chat history for the specified memory key.

        Args:
            memory_key (str): The key to identify the conversation memory.

        Returns:
            str | None: The chat history if the memory key exists, None otherwise.
        """
        return (
            self._memory_bank[memory_key].get_chat_history()
            if memory_key in self._memory_bank
            else ""
        )

    def get_chat_summary(self, memory_key: str) -> str | None:
        """
        Get the chat summary for the specified memory key.

        Args:
            memory_key (str): The key to identify the conversation memory.

        Returns:
            str | None: The chat summary if the memory key exists, None otherwise.
        """
        return (
            self._memory_bank[memory_key].get_chat_summary()
            if memory_key in self._memory_bank
            else ""
        )

    def clear_history(self, memory_key: str):
        """
        Clear the chat history for the specified memory key.

        Args:
            memory_key (str): The key to identify the conversation memory.
        """
        self._memory_bank[memory_key].clear_chat_history()

    def clear_summary(self, memory_key: str):
        """
        Clear the chat summary for the specified memory key.

        Args:
            memory_key (str): The key to identify the conversation memory.
        """
        self._memory_bank[memory_key].clear_chat_summary()

    def clear_entire_memory(self, memory_key: str):
        """
        Clear the entire conversation memory for the specified memory key.

        Args:
            memory_key (str): The key to identify the conversation memory.
        """
        self.clear_history(memory_key)
        self.clear_summary(memory_key)

    def append_to_memory(self, memory_key: str, messages: list[dict[str, str]]):
        """
        Append a message to the conversation memory for the specified memory key.

        Args:
            memory_key (str): The key to identify the conversation memory.
            role (str): The role of the message sender. Must be 'AI' or 'User'.
            message (str): The message to append to the conversation memory.

        Raises:
            ValueError: If the role is not 'AI' or 'User'.
        """
        if memory_key not in self._memory_bank:
            self._memory_bank[memory_key] = ConversationMemory(llm=self._llm, k=self._k)
        for message in messages:
            role = message["role"]
            content = message["content"]
            match role:
                case MemoryManager.MessageRoles.AI:
                    self._memory_bank[memory_key].insert_ai_message(content)
                case MemoryManager.MessageRoles.HUMAN:
                    self._memory_bank[memory_key].insert_user_message(content)
                case _:
                    raise ValueError("Role must be 'AI' or 'User'")

        self._memory_bank[memory_key].update_chat_summary()

    def __str__(self) -> str:
        """
        Get a string representation of the MemoryManager object.

        Returns:
            str: The string representation of the MemoryManager object.
        """
        output = "MEMORY INFORMATION:\n"
        output += "===================\n"
        i = 1
        for mk, val in self._memory_bank.items():
            output += f"{i}. {mk}: {len(val)} messages\n"
            i += 1
        return output
