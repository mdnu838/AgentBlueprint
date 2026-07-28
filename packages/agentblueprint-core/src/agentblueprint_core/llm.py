"""
LLM Provider abstractions and implementations.
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Dict
import os
from pydantic import BaseModel

from agentblueprint_core.tools import Tool

class LLMResponse(BaseModel):
    """Structured response from an LLM."""
    content: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> LLMResponse:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: User input prompt.
            system_prompt: System instruction.
            tools: List of available tools.
            history: Conversation history (optional).
            
        Returns:
            The structured response from the LLM, including content and usage.
        """
        pass

class MockLLM(LLMProvider):
    """A mock provider for testing."""
    
    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> LLMResponse:
        prefix = "ECHO"
        if system_prompt:
            prefix = f"ECHO ({system_prompt})"

        content = f"{prefix}: {prompt}"
        # Mock usage based on string length to simulate token usage in tests
        tokens = len(content.split())

        return LLMResponse(
            content=content,
            prompt_tokens=len(prompt.split()),
            completion_tokens=tokens,
            total_tokens=len(prompt.split()) + tokens,
            cost=0.0
        )

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

    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if history:
            # Append history (assuming history is in compatible format)
            # We might need to map roles if they differ, but standard is (user, assistant)
            messages.extend(history)
            
        messages.append({"role": "user", "content": prompt})
        
        openai_tools = None
        if tools:
            openai_tools = []
            for tool in tools:
                tool_def = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                    }
                }
                if tool.parameters:
                    tool_def["function"]["parameters"] = tool.parameters

                openai_tools.append(tool_def)
        
        try:
            kwargs = {
                "model": self.model_name,
                "messages": messages
            }
            if openai_tools:
                kwargs["tools"] = openai_tools

            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content or ""
            usage = response.usage

            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            total_tokens = usage.total_tokens if usage else 0

            # Very basic cost estimation for gpt-3.5-turbo (per 1k tokens)
            # Note: actual rates change and vary by exact model variant
            cost = 0.0
            if "gpt-3.5" in self.model_name:
                cost = (prompt_tokens / 1000.0) * 0.0005 + (completion_tokens / 1000.0) * 0.0015
            elif "gpt-4" in self.model_name:
                cost = (prompt_tokens / 1000.0) * 0.03 + (completion_tokens / 1000.0) * 0.06

            return LLMResponse(
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost=cost
            )
        except Exception as e:
            return LLMResponse(content=f"Error calling OpenAI: {str(e)}")

class AnthropicLLM(LLMProvider):
    """Anthropic API Provider."""

    def __init__(self, model_name: str = "claude-3-haiku-20240307"):
        self.model_name = model_name
        try:
            import anthropic
            self.client = anthropic.Anthropic()
        except ImportError:
            raise ImportError("anthropic package is not installed. Run `pip install anthropic`.")
        except Exception:
            self.client = anthropic.Anthropic()

    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> LLMResponse:
        messages = []
        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.messages.create(
                model=self.model_name,
                system=system_prompt,
                messages=messages,
                max_tokens=4096
            )

            content = response.content[0].text if response.content else ""

            prompt_tokens = response.usage.input_tokens
            completion_tokens = response.usage.output_tokens
            total_tokens = prompt_tokens + completion_tokens

            cost = 0.0
            if "claude-3-opus" in self.model_name:
                cost = (prompt_tokens / 1000000.0) * 15.0 + (completion_tokens / 1000000.0) * 75.0
            elif "claude-3-sonnet" in self.model_name:
                cost = (prompt_tokens / 1000000.0) * 3.0 + (completion_tokens / 1000000.0) * 15.0
            elif "claude-3-haiku" in self.model_name:
                cost = (prompt_tokens / 1000000.0) * 0.25 + (completion_tokens / 1000000.0) * 1.25

            return LLMResponse(
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost=cost
            )
        except Exception as e:
            return LLMResponse(content=f"Error calling Anthropic: {str(e)}")

class GeminiLLM(LLMProvider):
    """Google Gemini API Provider."""

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name
        try:
            import google.generativeai as genai
            self.genai = genai
            # Ensure API key is configured if available in env
            if os.environ.get("GEMINI_API_KEY"):
                genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel(self.model_name)
        except ImportError:
            raise ImportError("google-generativeai package is not installed. Run `pip install google-generativeai`.")

    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> LLMResponse:
        messages = []
        if history:
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"
                messages.append({"role": role, "parts": [msg["content"]]})

        messages.append({"role": "user", "parts": [prompt]})

        try:
            # Re-initialize model with system instruction if provided
            model = self.model
            if system_prompt:
                model = self.genai.GenerativeModel(self.model_name, system_instruction=system_prompt)

            response = model.generate_content(messages)
            content = response.text

            prompt_tokens = response.usage_metadata.prompt_token_count if hasattr(response, "usage_metadata") else 0
            completion_tokens = response.usage_metadata.candidates_token_count if hasattr(response, "usage_metadata") else 0
            total_tokens = response.usage_metadata.total_token_count if hasattr(response, "usage_metadata") else 0

            # Gemini cost estimation (using current general pricing for flash/pro)
            cost = 0.0
            if "gemini-1.5-flash" in self.model_name:
                cost = (prompt_tokens / 1000000.0) * 0.075 + (completion_tokens / 1000000.0) * 0.3
            elif "gemini-1.5-pro" in self.model_name:
                cost = (prompt_tokens / 1000000.0) * 3.5 + (completion_tokens / 1000000.0) * 10.5

            return LLMResponse(
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost=cost
            )
        except Exception as e:
            return LLMResponse(content=f"Error calling Gemini: {str(e)}")

class OllamaLLM(LLMProvider):
    """Local Ollama Provider."""

    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        try:
            import ollama
            self.client = ollama
        except ImportError:
            raise ImportError("ollama package is not installed. Run `pip install ollama`.")

    def generate(self, prompt: str, system_prompt: str = "", tools: List[Tool] = None, history: List[Dict[str, str]] = None) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat(model=self.model_name, messages=messages)

            content = response['message']['content']
            prompt_tokens = response.get('prompt_eval_count', 0)
            completion_tokens = response.get('eval_count', 0)
            total_tokens = prompt_tokens + completion_tokens

            return LLMResponse(
                content=content,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                cost=0.0  # Local models are free
            )
        except Exception as e:
            return LLMResponse(content=f"Error calling Ollama: {str(e)}")

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
        elif provider == "anthropic":
            return AnthropicLLM(model_name=model_name)
        elif provider == "gemini":
            return GeminiLLM(model_name=model_name)
        elif provider == "ollama":
            return OllamaLLM(model_name=model_name)
        elif provider == "mock" or provider == "echo":
            # We ignore model_name for mock currently
            return MockLLM()
        else:
            # Fallback or error
            raise ValueError(f"Unknown provider: {provider}")
