"""
Example demonstrating how to use the evaluation and prompt optimization framework.
"""
from agentblueprint_core.agent import Agent
from agentblueprint_eval.optimizer import PromptOptimizer
from agentblueprint_eval.evaluator import LLMJudge

def main():
    print("--- Running Evaluation & Optimization Example ---\n")

    # 1. Setup the initial agent (we use a mock for demonstration without API keys)
    agent = Agent(
        name="math_bot",
        model="mock:test",
        system_prompt="You are a helpful math bot."
    )

    # 2. Define a test set
    # Using mock, the output is 'ECHO (system_prompt): input'
    test_set = [
        {"input": "What is 2+2?", "expected_output": "ECHO (You are a helpful math bot.): What is 2+2?"}, # Should pass exact match initially
        {"input": "What is 3+3?", "expected_output": "6"}, # Should fail initially
    ]

    # 3. Simple Evaluation
    print("1. Running simple evaluation...")
    # Note: For real use, provide an openai:gpt-4 model string instead of None
    judge = LLMJudge(provider_model=None)

    input_text = test_set[0]["input"]
    actual = agent.run(input_text)
    expected = test_set[0]["expected_output"]

    res = judge.evaluate(input_text, actual, expected)
    print(f"Result for input '{input_text}': Score={res.score}, Reason={res.reasoning}\n")

    # 4. Prompt Optimization
    print("2. Running prompt optimization loop (mock)...")

    # Initialize optimizer (using mock for demonstration)
    optimizer = PromptOptimizer(
        optimizer_model="mock:opt",
        judge_model=None # exact match for demo
    )

    result = optimizer.optimize(
        agent=agent,
        test_set=test_set,
        iterations=2
    )

    print("\nOptimization Complete!")
    print(f"Best Score: {result.best_score}")
    print(f"Best Prompt: {result.best_prompt}")

if __name__ == "__main__":
    main()
