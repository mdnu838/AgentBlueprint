import pytest
from agentblueprint_eval.evaluator import LLMJudge

def test_llm_judge_disabled():
    judge = LLMJudge(provider_model=None)

    # Exact match pass
    res = judge.evaluate("input", "hello", "hello")
    assert res.score is True
    assert "Exact match fallback" in res.reasoning

    # Exact match fail
    res = judge.evaluate("input", "hello", "world")
    assert res.score is False

def test_llm_judge_mock():
    # Use the mock provider which just echoes
    judge = LLMJudge(provider_model="mock:test")

    # The mock returns ECHO (system_prompt): prompt
    # So it won't be formatted like Score: PASS, meaning it will likely fail parsing standardly
    # but we can test the fallback or error state.
    res = judge.evaluate("input", "actual", "expected")

    # Given the mock just echoes, it won't have PASS in it.
    assert res.score is False
    assert "ECHO" in res.reasoning
