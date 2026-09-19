"""
Local embedding model via Ollama.

Chat Model      -> generates language
Embedding Model -> represents meaning as vectors
"""

from langchain_ollama import OllamaEmbeddings
from audio_analytics.config import settings

def get_embeddings(model: str | None = None) -> OllamaEmbeddings:
    return OllamaEmbeddings(model=model or settings.embedding_model)