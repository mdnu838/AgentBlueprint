"""
Unit tests for AgentBlueprint LLM providers and structured output.
"""
import pytest
from unittest.mock import patch, MagicMock

from agentblueprint_core.llm import (
    LLMFactory,
    MockLLM,
    OpenAILLM,
    AnthropicLLM,
    GeminiLLM,
    OllamaLLM,
    LLMResponse
)

def test_mock_llm():
    provider = LLMFactory.create("mock:test")
    assert isinstance(provider, MockLLM)

    response = provider.generate("hello world", system_prompt="Sys")
    assert isinstance(response, LLMResponse)
    assert "ECHO (Sys): hello world" in response.content
    assert response.prompt_tokens == 2 # "hello world"
    assert response.completion_tokens > 0
    assert response.total_tokens > response.prompt_tokens
    assert response.cost == 0.0

@patch("openai.OpenAI")
def test_openai_llm(mock_openai):
    # Mocking openai client response
    mock_client = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "OpenAI response"
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 20
    mock_response.usage.total_tokens = 30

    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    provider = LLMFactory.create("openai:gpt-3.5-turbo")
    assert isinstance(provider, OpenAILLM)

    response = provider.generate("hello")
    assert isinstance(response, LLMResponse)
    assert response.content == "OpenAI response"
    assert response.prompt_tokens == 10
    assert response.completion_tokens == 20
    assert response.total_tokens == 30
    assert response.cost > 0.0

@patch("anthropic.Anthropic")
def test_anthropic_llm(mock_anthropic):
    mock_client = MagicMock()
    mock_message = MagicMock()
    mock_message.text = "Anthropic response"
    mock_response = MagicMock()
    mock_response.content = [mock_message]
    mock_response.usage.input_tokens = 15
    mock_response.usage.output_tokens = 25

    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client

    provider = LLMFactory.create("anthropic:claude-3-haiku-20240307")
    assert isinstance(provider, AnthropicLLM)

    response = provider.generate("hello")
    assert isinstance(response, LLMResponse)
    assert response.content == "Anthropic response"
    assert response.prompt_tokens == 15
    assert response.completion_tokens == 25
    assert response.total_tokens == 40
    assert response.cost > 0.0

@patch("os.environ.get")
@patch("google.generativeai.GenerativeModel")
def test_gemini_llm(mock_genai_model, mock_env_get):
    mock_env_get.return_value = "fake_key"

    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Gemini response"
    mock_response.usage_metadata.prompt_token_count = 5
    mock_response.usage_metadata.candidates_token_count = 10
    mock_response.usage_metadata.total_token_count = 15

    mock_model.generate_content.return_value = mock_response
    mock_genai_model.return_value = mock_model

    provider = LLMFactory.create("gemini:gemini-1.5-flash")
    assert isinstance(provider, GeminiLLM)

    provider.model = mock_model
    provider.genai.GenerativeModel = mock_genai_model

    response = provider.generate("hello")
    assert isinstance(response, LLMResponse)
    assert response.content == "Gemini response"
    assert response.prompt_tokens == 5
    assert response.completion_tokens == 10
    assert response.total_tokens == 15
    assert response.cost > 0.0

@patch("ollama.chat")
def test_ollama_llm(mock_ollama_chat):
    mock_ollama_chat.return_value = {
        'message': {'content': 'Ollama response'},
        'prompt_eval_count': 50,
        'eval_count': 100
    }

    provider = LLMFactory.create("ollama:llama3")
    assert isinstance(provider, OllamaLLM)

    response = provider.generate("hello")
    assert isinstance(response, LLMResponse)
    assert response.content == "Ollama response"
    assert response.prompt_tokens == 50
    assert response.completion_tokens == 100
    assert response.total_tokens == 150
    assert response.cost == 0.0
