from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model: str = "qwen3.5:0.8b"
    google_model: str = "gemini-2.5-flash"
    temperature: float = 0.5
    google_api_key: str | None = None 
    max_output_tokens: int = 1000

    # RAG
    embedding_model: str = "nomic-embed-text"
    chunk_size: int = 500
    chunk_overlap: int = 100
    knowledge_dir: str = "knowledge"
    top_k: int = 3

    # knowledge directory
    knowledge_dir: str = "src/knowledge"

settings = Settings()