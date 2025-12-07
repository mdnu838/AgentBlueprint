"""
Callback system for AgentBlueprint observability.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class CallbackHandler(ABC):
    """
    Abstract base class for handling execution events.
    """
    
    def on_workflow_start(self, name: str, input_data: Any) -> None:
        """Called when a workflow starts."""
        pass

    def on_workflow_end(self, name: str, output_data: Any) -> None:
        """Called when a workflow ends."""
        pass
        
    def on_agent_start(self, name: str, input_text: str) -> None:
        """Called when an agent starts execution."""
        pass

    def on_agent_end(self, name: str, response: str) -> None:
        """Called when an agent finishes execution."""
        pass
        
    def on_tool_start(self, name: str, input_args: Any) -> None:
        """Called when a tool triggers."""
        pass

    def on_tool_end(self, name: str, output: str) -> None:
        """Called when a tool finishes."""
        pass

class CallbackManager:
    """Helper to dispatch events to multiple handlers."""
    def __init__(self, handlers: list[CallbackHandler] = None):
        self.handlers = handlers or []

    def on_workflow_start(self, name: str, input_data: Any) -> None:
        for h in self.handlers: h.on_workflow_start(name, input_data)

    def on_workflow_end(self, name: str, output_data: Any) -> None:
        for h in self.handlers: h.on_workflow_end(name, output_data)

    def on_agent_start(self, name: str, input_text: str) -> None:
        for h in self.handlers: h.on_agent_start(name, input_text)

    def on_agent_end(self, name: str, response: str) -> None:
        for h in self.handlers: h.on_agent_end(name, response)
        
    def on_tool_start(self, name: str, input_args: Any) -> None:
        for h in self.handlers: h.on_tool_start(name, input_args)

    def on_tool_end(self, name: str, output: str) -> None:
        for h in self.handlers: h.on_tool_end(name, output)
