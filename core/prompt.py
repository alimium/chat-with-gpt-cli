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
        web_resources: str | None = None,
    ):
        system_msg = system_msg or DEFAULT_CONVERSATION_SYS_MSG
        template = ""
        if web_resources:
            template += f"WEB RESOURCES:\n{web_resources}\n\n"
        if summary:
            template += f"SUMMARY OF CONVERSATION:\n{summary}\n\n"
        template += f"{system_msg}\n"
        if history:
            template += f"{history}\n"
        template += f"Human: {input_}\nAI:"
        return template
