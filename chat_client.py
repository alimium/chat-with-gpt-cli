"""
Client for the chatbot service
"""

from timeit import default_timer as timer
import uuid

import grpc
from colorama import Fore, Style

from chat_pb2_grpc import ChatbotStub
from chat_pb2 import ConversationalRequest, ConversationalResponse


def run():
    """Run the chatbot client."""
    with grpc.insecure_channel("localhost:50011") as channel:
        stub = ChatbotStub(channel)
        session = str(uuid.uuid4())
        print(f"Session: {session}")

        while True:
            message = input("You: ")
            request = ConversationalRequest(session_uuid=session, input=message)
            token_counter = 0
            start_time = timer()
            for response in stub.Conversational(request):
                status = response.status
                match status:
                    case ConversationalResponse.Status.LOAD_HISTORY:
                        print(Fore.YELLOW + "Loading History...", end="\r")
                    case ConversationalResponse.Status.BUILD_PROMPT:
                        print(Fore.YELLOW + "Building Prompt...", end="\r")
                    case ConversationalResponse.Status.GENERATE_RESPONSE:
                        print(Fore.CYAN + response.token, flush=True, end="")
                        token_counter += 1
                    case ConversationalResponse.Status.UPDATE_MEMORY:
                        print(
                            Fore.YELLOW + "\nSaving conversation into memory...",
                            end="\r",
                        )
                    case ConversationalResponse.Status.FAILED:
                        print(Fore.RED + "An Error Occured!")
            print(
                Fore.RESET
                + Style.DIM
                + f"Generated {token_counter} tokens in {timer()-start_time:.2f} seconds"
                + Style.RESET_ALL
            )


if __name__ == "__main__":
    run()
