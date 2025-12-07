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
        return "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in self.messages])

class NoOpMemory(Memory):
    """Memory that stores nothing."""
    def add(self, role: str, content: str) -> None:
        pass
    
    def get_history(self) -> List[Dict[str, str]]:
        return []
        
    def get_context(self) -> str:
        return ""
