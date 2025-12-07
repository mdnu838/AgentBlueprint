"""
LLM Provider abstractions and implementations.
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict
import os

from agentblueprint_core.tools import Tool

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User input prompt.
            system_prompt: System instruction.
            tools: List of available tools.
            history: Conversation history (optional).
            
        Returns:
            The generated text response.
        """
        pass

class MockLLM(LLMProvider):
    """A mock provider for testing."""
    
    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> str:
        prefix = "ECHO"
        if system_prompt:
            prefix = f"ECHO ({system_prompt})"
        return f"{prefix}: {prompt}"

class OpenAILLM(LLMProvider):
    """OpenAI API Provider."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        try:
            import openai
            self.client = openai.OpenAI()
        except ImportError:
            raise ImportError("openai package is not installed. Run `pip install openai`.")
        except Exception:
            # Handle missing API key or other init errors generically
            # For now we assume env var OPENAI_API_KEY is set
            self.client = openai.OpenAI()

    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if history:
            # Append history (assuming history is in compatible format)
            # We might need to map roles if they differ, but standard is (user, assistant)
            messages.extend(history)
            
        messages.append({"role": "user", "content": prompt})
        
        # Simple tool definition (omitted for phase 1 of LLM integration - just text generation first)
        # TODO: Add tool calling support
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

class LLMFactory:
    """Factory to get the correct LLM provider."""
    
    @staticmethod
    def create(model_str: str) -> LLMProvider:
        """
        Create a provider instance from a model string.
        Format: provider:model_name (e.g., openai:gpt-4, mock:echo)
        """
        if ":" in model_str:
            provider, model_name = model_str.split(":", 1)
        else:
            # Default to mock if no provider specified, or assume openai?
            # Safer to default to mock for now to avoid accidental bills
            provider = "mock"
            model_name = model_str

        if provider == "openai":
            return OpenAILLM(model_name=model_name)
        elif provider == "mock" or provider == "echo":
            # We ignore model_name for mock currently
            return MockLLM()
        else:
            # Fallback or error
            raise ValueError(f"Unknown provider: {provider}")
