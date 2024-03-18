# Chat with GPT (CLI)

This is a simple CLI tool to chat with OpenAI GPT (Maybe other models are available in the future.)

## Instrunctions
1. run `pip install -r requirements.txt` to install the required packages.
2. create a `.env` file in the root directory and add the following:
```bash
GRPC_PORT=<your-desired-grpc-port>
GRPC_MAX_WORKERS=<max-workers>
OPENAI_API_KEY = <your-openai-api-key>
TAVILY_API_KEY = <your-tavily-api-key>
```
3. run `python chat_server.py` to start the server.
4. run `python chat_client.py` in another terminal to start the client.
5. Enjoy chatting with GPT from your terminal!

## Features
- OpenAI models
- gRPC server/client
- Response streaming
- Memory aware generation with chat summary
- Custom system messages
- Web search capability

## Warning!
*BEWARE THAT THE MEMORY MANAGER WILL USE CHAT HISTORY TO GENERATE CONVERSATION SUMMARY USING THE SAME LLM AS THE CHATBOT. ALSO WHEN CONSTRUCTING PROMPTS, CHAT HISTORY, CHAT SUMMARY AND THE SYSTEM MESSAGE ARE APPENDED TO THE PROMPT, MAKING LATER PROMPTS IN THE CONVERSATION LONGER. OVERAL TOKENS SENT IN OPENAI API CALLS ARE MUCH MORE THAN WHAT THE USER HAS ENTERED AS INPUT, SO DON'T LET THE BILLINGS SURPRISE YOU!*
