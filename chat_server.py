"""Chatbot Server"""

from concurrent import futures
import os
import logging
import grpc
from dotenv import load_dotenv

from chat_servicer import ChatbotServicerImpl
from chat_pb2_grpc import add_ChatbotServicer_to_server


def serve():
    """Start the server"""
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the server...")
    load_dotenv()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if tavily_api_key is None:
        raise ValueError("TAVILY_API_KEY is not set")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OpenAI API is not set")
    grpc_port = os.getenv("GRPC_PORT")
    if grpc_port is None:
        raise ValueError("GRPC_PORT is not set")
    grpc_max_workers = os.getenv("GRPC_MAX_WORKERS")
    if grpc_max_workers is None:
        logging.warning("GRPC_MAX_WORKERS is not set, using default value 10")
        grpc_max_workers = 10

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(grpc_max_workers)))
    add_ChatbotServicer_to_server(ChatbotServicerImpl(openai_api_key, tavily_api_key), server)
    server.add_insecure_port(f"[::]:{grpc_port}")
    server.start()
    logging.info("Server started at port %s", grpc_port)
    server.wait_for_termination()


serve()
