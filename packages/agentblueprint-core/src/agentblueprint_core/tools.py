"""
Tool base class and registry for AgentBlueprint.

This module provides the core abstraction for tools that agents can use
to perform specific tasks.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class Tool(ABC):
    """
    Base class for all tools that agents can use.
    
    Tools are callable units of functionality that agents can invoke
    to perform specific tasks (search, calculate, API calls, etc.)
    
    Attributes:
        name: Unique identifier for the tool
        description: Human-readable description of what the tool does
        parameters: Optional parameter schema for the tool
        
    Example:
        >>> class CalculatorTool(Tool):
        ...     name = "calculator"
        ...     description = "Performs basic math calculations"
        ...     
        ...     def run(self, expression: str) -> float:
        ...         return eval(expression)
        ...
        >>> calc = CalculatorTool()
        >>> calc.run("2 + 2")
        4.0
    """
    
    name: str
    description: str
    parameters: Optional[dict[str, Any]] = None
    
    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            Tool-specific output
            
        Raises:
            NotImplementedError: This is an abstract method
        """
        pass
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert tool to dictionary for serialization.
        
        Returns:
            Dictionary containing tool metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


class ToolRegistry:
    """
    Global registry for tool discovery and management.
    
    Provides a centralized location for registering and
    retrieving tools by name.
    
    Example:
        >>> class MyTool(Tool):
        ...     name = "my_tool"
        ...     description = "Does something"
        ...     def run(self, x): return x
        ...
        >>> tool = MyTool()
        >>> ToolRegistry.register(tool)
        >>> retrieved = ToolRegistry.get("my_tool")
        >>> retrieved.name
        'my_tool'
    """
    
    _tools: dict[str, Tool] = {}
    
    @classmethod
    def register(cls, tool: Tool) -> None:
        """
        Register a tool in the registry.
        
        Args:
            tool: Tool instance to register
        """
        cls._tools[tool.name] = tool
    
    @classmethod
    def get(cls, name: str) -> Optional[Tool]:
        """
        Get a tool by name.
        
        Args:
            name: Name of the tool to retrieve
            
        Returns:
            Tool instance if found, None otherwise
        """
        return cls._tools.get(name)
    
    @classmethod
    def list_all(cls) -> list[Tool]:
        """
        List all registered tools.
        
        Returns:
            List of all registered tool instances
        """
        return list(cls._tools.values())
    
    @classmethod
    def clear(cls) -> None:
        """
        Clear the registry.
        
        This is mainly useful for testing to ensure a clean state.
        """
        cls._tools.clear()
