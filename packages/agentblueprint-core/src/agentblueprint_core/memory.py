"""
Memory systems for AgentBlueprint agents.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class Memory(BaseModel, ABC):
    """Abstract base class for agent memory."""
    
    @abstractmethod
    def add(self, role: str, content: str) -> None:
        """Add a message to memory."""
        pass
    
    @abstractmethod
    def get_history(self) -> List[Dict[str, str]]:
        """Retrieve full conversation history."""
        pass
    
    @abstractmethod
    def get_context(self) -> str:
        """Retrieve history formatted as a context string."""
        pass

class SimpleMemory(Memory):
    """
    Simple in-memory buffer of messages.
    """
    messages: List[Dict[str, str]] = Field(default_factory=list)
    
    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        
    def get_history(self) -> List[Dict[str, str]]:
        return self.messages
    
    def get_context(self) -> str:
        return "\n".join(f"{msg['role'].upper()}: {msg['content']}" for msg in self.messages)

class NoOpMemory(Memory):
    """Memory that stores nothing."""
    def add(self, role: str, content: str) -> None:
        pass
    
    def get_history(self) -> List[Dict[str, str]]:
        return []
        
    def get_context(self) -> str:
        return ""

try:
    from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
    from sqlalchemy.orm import declarative_base, sessionmaker
    import datetime

    MemoryBase = declarative_base()

    class Message(MemoryBase):
        __tablename__ = 'memory_messages'
        id = Column(Integer, primary_key=True)
        session_id = Column(String(255), index=True)
        role = Column(String(50))
        content = Column(Text)
        timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

except ImportError:
    MemoryBase = None
    Message = None

_memory_engine_cache = {}

def _get_memory_engine_and_session(db_url: str):
    if MemoryBase is None:
        raise ImportError("sqlalchemy is required for SQLMemory. Install with `pip install sqlalchemy`.")

    if db_url not in _memory_engine_cache:
        engine = create_engine(db_url)
        MemoryBase.metadata.create_all(engine)
        session_maker = sessionmaker(bind=engine)
        _memory_engine_cache[db_url] = (engine, session_maker)

    return _memory_engine_cache[db_url]


class SQLMemory(Memory):
    """
    SQL-backed memory using SQLAlchemy.
    Stores messages with a session_id to distinguish conversations.
    """
    db_url: str
    session_id: str = "default"

    engine: Any = Field(default=None, exclude=True)
    session_maker: Any = Field(default=None, exclude=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.engine, self.session_maker = _get_memory_engine_and_session(self.db_url)

    def add(self, role: str, content: str) -> None:
        session = self.session_maker()
        try:
            msg = Message(session_id=self.session_id, role=role, content=content)
            session.add(msg)
            session.commit()
        finally:
            session.close()

    def get_history(self) -> List[Dict[str, str]]:
        session = self.session_maker()
        try:
            messages = session.query(Message).filter_by(session_id=self.session_id).order_by(Message.timestamp).all()
            return [{"role": msg.role, "content": msg.content} for msg in messages]
        finally:
            session.close()

    def get_context(self) -> str:
        history = self.get_history()
        return "\n".join(f"{msg['role'].upper()}: {msg['content']}" for msg in history)
