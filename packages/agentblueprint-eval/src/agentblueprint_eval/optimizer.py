import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from agentblueprint_core.agent import Agent
from agentblueprint_core.llm import LLMFactory
from agentblueprint_eval.evaluator import LLMJudge

logger = logging.getLogger(__name__)

class OptimizationResult(BaseModel):
    best_prompt: str
    best_score: float
    history: List[Dict[str, Any]]

class PromptOptimizer:
    def __init__(self, optimizer_model: str, judge_model: Optional[str] = None):
        """
        Initializes the PromptOptimizer.

        Args:
            optimizer_model: The LLM model to use for generating new prompts (e.g., 'openai:gpt-4').
            judge_model: The LLM model to use for evaluating the results. If None, exact match is used.
        """
        self.optimizer_llm = LLMFactory.create(optimizer_model)
        self.judge = LLMJudge(provider_model=judge_model)

    def optimize(
        self,
        agent: Agent,
        test_set: List[Dict[str, str]],
        iterations: int = 3,
        criteria: str = "Assess if the actual output meets the expected output."
    ) -> OptimizationResult:
        """
        Iteratively optimizes the agent's system prompt to maximize performance on the test set.

        Args:
            agent: The agent to optimize.
            test_set: A list of dicts with 'input' and 'expected_output'.
            iterations: Number of optimization loops to run.
            criteria: The criteria the judge should use to evaluate the output.

        Returns:
            An OptimizationResult containing the best prompt found and the history of the optimization.
        """
        best_prompt = agent.system_prompt
        best_score = 0.0
        history = []

        current_prompt = best_prompt

        for i in range(iterations):
            logger.info(f"Starting iteration {i+1}/{iterations} with prompt: {current_prompt}")

            # 1. Evaluate current prompt
            agent.system_prompt = current_prompt
            pass_count = 0
            failures = []

            for example in test_set:
                input_text = example['input']
                expected_output = example['expected_output']

                # We do not pass callbacks here for simplicity, though they could be added
                try:
                    actual_output = agent.run(input_text=input_text)
                    result = self.judge.evaluate(
                        input_text=input_text,
                        actual_output=actual_output,
                        expected_output=expected_output,
                        criteria=criteria
                    )

                    if result.score:
                        pass_count += 1
                    else:
                        failures.append({
                            "input": input_text,
                            "expected": expected_output,
                            "actual": actual_output,
                            "reason": result.reasoning
                        })
                except Exception as e:
                    failures.append({
                        "input": input_text,
                        "expected": expected_output,
                        "actual": f"Error: {str(e)}",
                        "reason": "Agent execution failed."
                    })

            # Calculate score
            score = pass_count / len(test_set) if test_set else 0.0

            iteration_data = {
                "iteration": i + 1,
                "prompt": current_prompt,
                "score": score,
                "failures": failures
            }
            history.append(iteration_data)

            if score > best_score:
                best_score = score
                best_prompt = current_prompt

            # If perfect score, we can stop early
            if score == 1.0:
                logger.info("Perfect score achieved. Stopping optimization early.")
                break

            # 2. Propose new prompt based on failures
            if i < iterations - 1 and failures:
                current_prompt = self._generate_new_prompt(current_prompt, failures, criteria)

        # Restore the best prompt to the agent
        agent.system_prompt = best_prompt

        return OptimizationResult(
            best_prompt=best_prompt,
            best_score=best_score,
            history=history
        )

    def _generate_new_prompt(self, current_prompt: str, failures: List[Dict[str, str]], criteria: str) -> str:
        """Uses the optimizer LLM to suggest a better system prompt."""

        system_instructions = (
            "You are an expert Prompt Engineer. Your task is to optimize a system prompt for an AI agent.\n"
            "You will be given the CURRENT PROMPT, the EVALUATION CRITERIA, and a list of FAILURE CASES where the agent failed.\n"
            "Analyze the failures to understand what the agent did wrong. Then, write a NEW PROMPT that addresses these issues.\n"
            "Your output MUST contain ONLY the new prompt, with no additional explanation or markdown formatting."
        )

        failures_text = ""
        for idx, f in enumerate(failures):
            failures_text += (
                f"Failure {idx+1}:\n"
                f"Input: {f['input']}\n"
                f"Expected: {f['expected']}\n"
                f"Actual: {f['actual']}\n"
                f"Reasoning: {f['reason']}\n\n"
            )

        prompt = (
            f"CURRENT PROMPT:\n{current_prompt}\n\n"
            f"EVALUATION CRITERIA:\n{criteria}\n\n"
            f"FAILURE CASES:\n{failures_text}\n"
            "Generate the NEW PROMPT below:"
        )

        try:
            new_prompt = self.optimizer_llm.generate(prompt=prompt, system_prompt=system_instructions)
            return new_prompt.strip()
        except Exception as e:
            logger.error(f"Failed to generate new prompt: {e}")
            return current_prompt # Fallback to current if generation fails
