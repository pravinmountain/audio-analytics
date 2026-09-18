import json 
from audio_analytics.conversation.store import ConversatioStore
from langchain_core.messages import AIMessage, HumanMessage
from audio_analytics.llm.llm_client import LLM 


class ConversationEngine:
    """Multi-turn chat engine"""

    def __init__(self, llm: LLM | None = None, store: ConversatioStore | None = None) -> None:
        self.llm = llm or LLM("ollama")
        self.store = store or ConversatioStore()

    def send_message(self, query: str, conversation_id: str | None = None) -> str:
        if conversation_id is None:
            conversation_id = self.store.create_conversation()
        self.store.append(conversation_id, "human", query)
        history = self.retrieve_conv_hist(conversation_id)
        messages = self.contruct_message(history)
        ai_text = self.invoke(messages)
        self.store_response(conversation_id, ai_text)
        return self.return_response(conversation_id, ai_text)

    def retrieve_conv_hist(self, conversation_id: str) -> list:
        return self.store.get_messages(conversation_id)

    @staticmethod
    def contruct_message(history: list) -> list:
        messages = []
        for msg in history:
            cls = HumanMessage if msg.role == "human" else AIMessage
            messages.append(cls(content=msg.content))
        return messages

    def invoke(self, messages: list) -> str:
        return self.llm.invoke(messages).content

    def store_response(self, conversation_id: str, ai_text: str) -> None:
        self.store.append(conversation_id, "ai", ai_text)

    @staticmethod
    def return_response(conversation_id: str, ai_text: str) -> str:
        return json.dumps({"conversation_id": conversation_id, "response": ai_text})


engine = ConversationEngine()
reply = engine.send_message("Hi! How are you?")   # starts a new conversation
print(reply)
data = json.loads(reply)
reply2 = engine.send_message("What did I just say?", data["conversation_id"])  # multi-turn
print(reply2)

