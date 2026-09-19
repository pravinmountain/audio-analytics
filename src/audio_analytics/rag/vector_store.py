from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class VectorStore:
    def __init__(self, embeddings, index_dir: str = "vector_index") -> None:
        self.embeddings = embeddings
        self.index_dir = Path(index_dir)
        self._index: FAISS | None = None

    @property 
    def index(self) -> FAISS:
        if self._index is None:
            raise RuntimeError("VectorStore index is not loaded. Call load_index() first.")
        return self._index

    def build(self, chunks: list[Document]) -> None:
        if not chunks:
            raise ValueError("No chunks to index.")
        self._index = FAISS.from_documents(chunks, self.embeddings)
        self.save()

    def load(self) -> bool:
        if not (self.index_dir / "index.faiss").exists():
            return False
        self._index = FAISS.load_local(str(self.index_dir), self.embeddings)
        return True

    def save(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self._index.save_local(str(self.index_dir))

    def search(self, query: str, top_k: int = 3) -> list[Document]:
        if self._index is None:
            raise RuntimeError("VectorStore index is not loaded. Call load_index() first.")
        return self._index.similarity_search(query, k=top_k)
