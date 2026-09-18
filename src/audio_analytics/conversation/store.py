import threading
import time 
import uuid 
import sqlite3
from pathlib import Path 
from dataclasses import dataclass, field

@dataclass
class Message:
    role: str 
    content: str 
    created_at: float = field(default_factory=time.time)

class ConversatioStore:
    """In-memory multi-turn conversation storage.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._conversations: dict[str, list[Message]] = {}

    def create_conversation(self) -> str:
        conversation_id = str(uuid.uuid4())
        with self._lock:
            self._conversations[conversation_id] = []
        return conversation_id

    def append(self, conversation_id: str, role: str, content: str) -> None: 
        with self._lock:
            self._conversations.setdefault(conversation_id, []).append(Message(role, content))

    def get_messages(self, conversation_id: str) -> list[Message]:
        with self._lock:
            return list(self._conversations.get(conversation_id, []))

    def clear(self, conversation_id: str) -> None:
        with self._lock:
            self._conversations.pop(conversation_id, None)

class ConversationRepository:
    """
    Conversation storage using SQLite 
    """
    def __init__(self, db_path: str | Path = "conversation.db") -> None:
        self._db_path = str(db_path)
        self._lock = threading.Lock()
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn 

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE OF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    created_at REAL NOT NULL
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id),
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at REAL NOT NULL
                );
            """)

    def create_conversation(self) -> str: 
        conversation_id = str(uuid.uuid4())
        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO conversations (id, created_at) VALUES (?, ?)",
                (conversation_id, time.time()),
            )
        return conversation_id

    def append(self, conversation_id: str, role: str, content: str) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (conversation_id, role, content, time.time()),
            )

    def get_message(self, conversation_id: str) -> list[Message]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content, created_at FROM messages WHERE conversation_id = ? ORDER BY id",
                (conversation_id,),
            ).fetchall()
        return [Message(row["role"], row["content"], row["created_at"]) for row in rows]