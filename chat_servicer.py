"""This module holds the implementation of the ChatbotServicer class"""

from langchain_openai import ChatOpenAI

from core import MemoryManager
from core import PromptEngine

from chat_pb2_grpc import ChatbotServicer
from chat_pb2 import ConversationalResponse


class ChatbotServicerImpl(ChatbotServicer):
    """
    This class is the implementation of the ChatbotServicer class.
    """

    def __init__(self, openai_api_key: str) -> None:
        self.openai_api_key = openai_api_key
        self.memory_manager: MemoryManager | None = None
        self.prompt_engine: PromptEngine | None = None

    def _llm_factory(self, openai_api_key: str):
        return ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo", streaming=True)  # type: ignore

    def Conversational(self, request, context):
        session = request.session_uuid
        input_ = request.input
        llm = self._llm_factory(self.openai_api_key)

        yield ConversationalResponse(status=ConversationalResponse.Status.LOAD_HISTORY)
        if self.memory_manager is None:
            self.memory_manager = MemoryManager(llm=llm)
        history = self.memory_manager.get_chat_history(session)
        summary = self.memory_manager.get_chat_summary(session)

        yield ConversationalResponse(status=ConversationalResponse.Status.BUILD_PROMPT)
        if self.prompt_engine is None:
            self.prompt_engine = PromptEngine()
        prompt = self.prompt_engine.generate_prompt(
            input_=input_, history=history, summary=summary
        )

        response = ""
        for token in llm.stream(input=prompt):
            response += token.content  # type: ignore
            yield ConversationalResponse(status=ConversationalResponse.Status.GENERATE_RESPONSE, token=token.content)  # type: ignore

        yield ConversationalResponse(status=ConversationalResponse.Status.UPDATE_MEMORY)
        conversation_iteration = [
            {"role": MemoryManager.MessageRoles.HUMAN, "content": input_},
            {"role": MemoryManager.MessageRoles.AI, "content": response},
        ]
        self.memory_manager.append_to_memory(session, conversation_iteration)

        yield ConversationalResponse(status=ConversationalResponse.Status.FINISHED)
