import pytest
from agentblueprint_core.agent import Agent
from agentblueprint_eval.optimizer import PromptOptimizer

def test_prompt_optimizer_mock():
    # We use mock LLMs to test the flow without API calls
    optimizer = PromptOptimizer(optimizer_model="mock:opt", judge_model=None)

    agent = Agent(name="test", model="mock:agent", system_prompt="initial prompt")

    test_set = [
        {"input": "in1", "expected_output": "ECHO (initial prompt): in1"}, # This should pass since agent mock returns ECHO (initial prompt): in1
        {"input": "in2", "expected_output": "wrong"} # This should fail
    ]

    result = optimizer.optimize(agent, test_set, iterations=2)

    # First iteration should run, score should be 0.5 (1 pass, 1 fail)
    # Because there are failures, it will propose a new prompt using mock:opt
    # The new prompt will be ECHO (...): CURRENT PROMPT...

    assert len(result.history) == 2
    assert result.history[0]["score"] == 0.5
    assert len(result.history[0]["failures"]) == 1

    # Best score shouldn't be worse than first iteration
    assert result.best_score >= 0.5
    assert agent.system_prompt == result.best_prompt
