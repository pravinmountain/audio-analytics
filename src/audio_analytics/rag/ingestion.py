from pathlib import Path 
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from audio_analytics.config import settings

class DocumentLoader:
    """Loads plain-text files from directory."""

    def load(self, directory: str) -> list[Document]:
        """Load documents from a directory."""
        docs = []
        for path in sorted(Path(directory).glob("*.txt")):
            docs.append(Document(
                page_content=path.read_text(encoding="utf-8"), 
                metadata={"source": path.name}
            ))
        if not docs:
            raise FileNotFoundError(f"No .txt files found in directory: {directory}")
        return docs

class Chunker:

    def __init__(self, chunk_size: int | None = None, chunk_overlap: int | None = None) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size or settings.chunk_size, 
            chunk_overlap=chunk_overlap or settings.chunk_overlap,
            separators=["\n\n", "\n", " ", "", ". "],
        )

    def split(self, documents: list[Document]) -> list[Document]:
        """Split documents into chunks."""
        chunks = self.splitter.split_documents(documents)
        for i, chunk in enumerate(chunks, start=1):
            chunk.metadata["chunk_id"] = f"chunk-{i:03d}"
        return chunks 
    
    @staticmethod
    def load_and_chunk(directory: str | Path) -> list[Document]:
        return Chunker().split(DocumentLoader().load(directory))
