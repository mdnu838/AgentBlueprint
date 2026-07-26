"""
Tool base class and registry for AgentBlueprint.

This module provides the core abstraction for tools that agents can use
to perform specific tasks.
"""

from abc import ABC, abstractmethod
import importlib.metadata
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


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


class VectorSearchTool(Tool):
    """
    Tool for searching a vector database.
    """
    name: str = "vector_search"
    description: str = "Search a knowledge base for relevant information."

    def __init__(self, vector_store: Any, top_k: int = 3, **data):
        super().__init__(**data)
        self.vector_store = vector_store
        self.top_k = top_k
        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                }
            },
            "required": ["query"]
        }

    def run(self, query: str, **kwargs) -> str:
        """Execute the search."""
        try:
            results = self.vector_store.search(query, top_k=self.top_k)
            if not results:
                return "No relevant information found."

            formatted = []
            for i, res in enumerate(results):
                text = res.get('text', '')
                meta = res.get('metadata', {})
                score = res.get('score', 0.0)
                formatted.append(f"Result {i+1} (Score: {score:.2f}):\n{text}")

            return "\n\n".join(formatted)
        except Exception as e:
            return f"Error during vector search: {str(e)}"
    @classmethod
    def load_plugins(cls) -> None:
        """
        Discover and load tools from installed python packages using entry points.

        Looks for the 'agentblueprint.tools' entry point group.
        Each entry point should point to a Tool class or instance.
        """
        try:
            entry_points = importlib.metadata.entry_points(group="agentblueprint.tools")
        except TypeError:
            # Fallback for older python versions if needed
            entry_points_all = importlib.metadata.entry_points()
            entry_points = entry_points_all.get("agentblueprint.tools", [])

        for ep in entry_points:
            try:
                plugin = ep.load()
                # If it's a class (subclass of Tool), instantiate it
                if isinstance(plugin, type) and issubclass(plugin, Tool):
                    cls.register(plugin())
                # If it's an instance of Tool
                elif isinstance(plugin, Tool):
                    cls.register(plugin)
                else:
                    logger.warning(f"Plugin {ep.name} is not a valid Tool: {plugin}")
            except Exception as e:
                logger.error(f"Failed to load plugin {ep.name}: {e}")
