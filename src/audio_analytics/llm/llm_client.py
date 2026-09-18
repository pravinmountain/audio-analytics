from audio_analytics.config import settings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama


class LLM:
    """Build chat model for a provider ('ollama' or 'gemini')"""

    PROVIVERS = ("ollama", "gemini")

    def __init__(self, provider: str = "ollama", model: str | None = None):
        if provider not in self.PROVIVERS:
            raise ValueError(f"Unsupported provider {provider!r}; choose from {self.PROVIVERS}")
        self.provider = provider
        self._model = self._build(model)

    def _build(self, model: str | None = None) -> BaseChatModel:
        if self.provider == "ollama":
            return ChatOllama(
                model=model or settings.model,
                temperature=settings.temperature,
                max_tokens=settings.max_output_tokens
            )
        return ChatGoogleGenerativeAI(
            model=model or settings.model,
            temperature=settings.temperature,
            max_tokens=settings.max_output_tokens
        )

    def invoke(self, message):
        return self._model.invoke(message)
