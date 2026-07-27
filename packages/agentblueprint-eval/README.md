# agentblueprint-eval

Evaluation and prompt optimization tools for AgentBlueprint.

This package provides:
- Auto-Evaluation framework (LLM-as-a-judge)
- Prompt optimization utilities

## Installation

This package is part of the AgentBlueprint monorepo and is installed automatically with the main toolkit.

## Auto-Evaluation (LLM-as-a-Judge)

The `LLMJudge` class allows you to evaluate agent outputs against expected outputs using an LLM (or fallback to exact string matching if no LLM provider is specified).

```python
from agentblueprint_eval import LLMJudge

# Using a configured LLM provider
judge = LLMJudge(provider_model="openai:gpt-4o")

result = judge.evaluate(
    input_text="What is the capital of France?",
    actual_output="The capital of France is Paris.",
    expected_output="Paris",
    criteria="Check if the actual output contains the correct expected answer."
)

print(result.score)      # True/False
print(result.reasoning)  # LLM reasoning
```

## Prompt Optimization

The `PromptOptimizer` iteratively improves an agent's system prompt by running it against a test set, evaluating failures, and using an LLM to propose better instructions.

```python
from agentblueprint_core import Agent
from agentblueprint_eval import PromptOptimizer

agent = Agent(name="test", model="openai:gpt-3.5-turbo", system_prompt="You are a helpful bot.")
test_set = [
    {"input": "What is 2+2?", "expected_output": "4"},
    {"input": "What is the capital of Japan?", "expected_output": "Tokyo"},
]

optimizer = PromptOptimizer(optimizer_model="openai:gpt-4o", judge_model="openai:gpt-4o")

result = optimizer.optimize(
    agent=agent,
    test_set=test_set,
    iterations=3,
    criteria="Check if the output is exactly the expected answer."
)

print(f"Best prompt found: {result.best_prompt}")
```
