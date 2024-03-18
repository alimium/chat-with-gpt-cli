"""This module holds the implementation of the ChatbotServicer class"""
import logging

from colorama import Fore, Style
from langchain_openai import ChatOpenAI
from langchain_community.retrievers.tavily_search_api import TavilySearchAPIRetriever, SearchDepth

from core import MemoryManager
from core import PromptEngine

from chat_pb2_grpc import ChatbotServicer
from chat_pb2 import ConversationalResponse


class ChatbotServicerImpl(ChatbotServicer):
    """
    This class is the implementation of the ChatbotServicer class.
    """

    def __init__(self, openai_api_key: str, tavily_api_key:str) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.openai_api_key = openai_api_key
        self.tavily_api_key = tavily_api_key
        self.memory_manager: MemoryManager | None = None
        self.prompt_engine: PromptEngine | None = None


    def _llm_factory(self, openai_api_key: str):
        # type: ignore
        return ChatOpenAI(api_key=openai_api_key, model="gpt-4-turbo-preview", streaming=True)

    def Conversational(self, request, context):
        session = request.session_uuid
        input_ = request.input
        llm = self._llm_factory(self.openai_api_key)
        web_retriever = TavilySearchAPIRetriever(api_key=self.tavily_api_key, k=5, search_depth=SearchDepth.ADVANCED)

        yield ConversationalResponse(status=ConversationalResponse.Status.LOAD_HISTORY)
        if self.memory_manager is None:
            self.memory_manager = MemoryManager(llm=llm)
        history = self.memory_manager.get_chat_history(session)
        summary = self.memory_manager.get_chat_summary(session)

        yield ConversationalResponse(status=ConversationalResponse.Status.WEB_SEARCH)
        try:
            search_query = "Chat summary:\n"+summary + "\nCurrent prompt: " + \
                input_ if summary else "\nCurrent prompt: " + input_
            web_search_results = web_retriever.invoke(input=search_query)
        except Exception as e:
            self.logger.error("Failed on web search", exc_info=e)
            return (yield ConversationalResponse(status=ConversationalResponse.Status.FAILED))
        web_resources = None
        if web_search_results:
            web_resources = "\n\n".join([f"{result.metadata['source']}: {result.page_content}" for result in web_search_results])

        yield ConversationalResponse(status=ConversationalResponse.Status.BUILD_PROMPT)
        if self.prompt_engine is None:
            self.prompt_engine = PromptEngine()
        prompt = self.prompt_engine.generate_prompt(
            input_=input_, history=history, summary=summary, web_resources=web_resources
        )
        self.logger.debug("Generated prompt: \n%s%s%s%s",Fore.GREEN,Style.BRIGHT,prompt,Style.RESET_ALL)
        try:
            response = ""
            for token in llm.stream(input=prompt):
                response += token.content  # type: ignore
                yield ConversationalResponse(status=ConversationalResponse.Status.GENERATE_RESPONSE, token=token.content)  # type: ignore
        except Exception as e:
            self.logger.error("Failed on generating response", exc_info=e)
            return (yield ConversationalResponse(status=ConversationalResponse.Status.FAILED))
        
        yield ConversationalResponse(status=ConversationalResponse.Status.UPDATE_MEMORY)
        try:
            conversation_iteration = [
                {"role": MemoryManager.MessageRoles.HUMAN, "content": input_},
                {"role": MemoryManager.MessageRoles.AI, "content": response},
            ]
            self.memory_manager.append_to_memory(session, conversation_iteration)
        except Exception as e:
            self.logger.error("Failed on updating memory", exc_info=e)
            return (yield ConversationalResponse(status=ConversationalResponse.Status.FAILED))
        
        yield ConversationalResponse(status=ConversationalResponse.Status.FINISHED, used_sources=[result.metadata['source'] for result in web_search_results] if web_search_results else [])
