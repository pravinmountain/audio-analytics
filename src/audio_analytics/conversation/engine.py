import json 

from langchain_core.messages import AIMessage, HumanMessage
from audio_analytics.llm.llm_client import LLM 


class ConversationEngine:
    """Multi-turn chat engine"""

    def __init__(self, llm: LLM | None = None) -> None:
        self.llm = llm or LLM("ollama")

    def send_message(self, query: str, conversation_id: str | None = None) -> str:
        if conversation_id is None:
            conversation_id = self.st

    def retrieve_conv_hist():
        ...

    def contruct_message(request):
        ...

    def invoke():
        ...

    def store_response():
        ... 

    def return_response():
        ...

