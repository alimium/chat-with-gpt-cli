from .constants import DEFAULT_CONVERSATION_SYS_MSG


class PromptEngine:
    def __init__(self, llm: str | None = None) -> None:
        self.llm = llm

    def generate_prompt(
        self,
        input_: str,
        system_msg: str | None = None,
        history: str | None = None,
        summary: str | None = None,
    ):
        system_msg = DEFAULT_CONVERSATION_SYS_MSG if system_msg is None else system_msg
        template = ""
        if summary:
            template += f"SUMMARY OF CONVERSATION:\n{summary}\n\n"
        template += f"{system_msg}\n"
        if history:
            template += f"{history}\n"
        template += f"Human: {input_}\nAI:"
        return template
