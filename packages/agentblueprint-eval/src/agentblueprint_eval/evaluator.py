from typing import Optional, Dict, Any, Union
from pydantic import BaseModel
from agentblueprint_core.llm import LLMProvider, LLMFactory

class EvaluationResult(BaseModel):
    score: Union[bool, float]
    reasoning: str

class LLMJudge:
    def __init__(self, provider_model: Optional[str] = None):
        """
        Initializes the LLMJudge.

        Args:
            provider_model: The LLM provider string (e.g., 'openai:gpt-4').
                            If None, evaluation acts as an exact match or disabled mode.
        """
        self.provider_model = provider_model
        self.llm = LLMFactory.create(provider_model) if provider_model else None

    def evaluate(self, input_text: str, actual_output: str, expected_output: str, criteria: str = "Assess if the actual output meets the expected output.") -> EvaluationResult:
        """
        Evaluates an output.
        """
        if not self.llm:
            # Fallback to exact match when no LLM is configured
            is_match = actual_output.strip() == expected_output.strip()
            return EvaluationResult(
                score=is_match,
                reasoning="Exact match fallback (no LLM configured)."
            )

        system_prompt = (
            "You are an impartial judge evaluating the output of an AI agent.\n"
            "You will be given the Input to the agent, the Actual Output it produced, "
            "the Expected Output (reference), and the Evaluation Criteria.\n"
            "Your response MUST be in exactly two lines:\n"
            "Line 1: Score: PASS or FAIL\n"
            "Line 2: Reasoning: <your brief reasoning>\n"
            "Follow these instructions exactly."
        )

        prompt = (
            f"Input:\n{input_text}\n\n"
            f"Expected Output:\n{expected_output}\n\n"
            f"Actual Output:\n{actual_output}\n\n"
            f"Criteria:\n{criteria}\n"
        )

        try:
            response_text = self.llm.generate(prompt=prompt, system_prompt=system_prompt)
            return self._parse_response(response_text)
        except Exception as e:
            return EvaluationResult(score=False, reasoning=f"Evaluation failed: {str(e)}")

    def _parse_response(self, response_text: str) -> EvaluationResult:
        """Parses the judge's response into an EvaluationResult."""
        lines = [line.strip() for line in response_text.strip().split('\n') if line.strip()]

        score = False
        reasoning = "Failed to parse judge output."

        for line in lines:
            if line.upper().startswith("SCORE:"):
                score_str = line[len("SCORE:"):].strip().upper()
                if "PASS" in score_str:
                    score = True
            elif line.upper().startswith("REASONING:"):
                reasoning = line[len("REASONING:"):].strip()

        # If standard parsing fails but we still have text
        if reasoning == "Failed to parse judge output." and lines:
            reasoning = " ".join(lines)

        return EvaluationResult(score=score, reasoning=reasoning)
