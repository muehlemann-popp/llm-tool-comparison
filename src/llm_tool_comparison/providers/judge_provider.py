"""Judge provider for evaluating LLM responses using GPT-4.1."""

import json
from typing import List
from openai import OpenAI
from haystack.tools import Tool

from .base import ConversationResult
from ..config.settings import settings


class JudgeProvider:
    """Evaluates LLM responses for quality and completeness using GPT-4.1."""

    def __init__(self, model_name: str = "gpt-4.1"):
        """Initialize the judge provider.

        Args:
            model_name: Model to use for judging (default: gpt-4.1)
        """
        self.model_name = model_name
        self.client = OpenAI(api_key=settings.openai_api_key)

    def evaluate_response(
        self,
        result: ConversationResult,
        original_query: str,
        available_tools: List[Tool]
    ) -> ConversationResult:
        """Evaluate response quality and update result with scores.

        Args:
            result: The ConversationResult to evaluate
            original_query: The original user query
            available_tools: List of tools that were available

        Returns:
            Updated ConversationResult with judge_score and judge_evaluation
        """
        # Build tool descriptions
        tool_descriptions = "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in available_tools
        ])

        # Build tool calls summary
        tool_calls_summary = "\n".join([
            f"- {tc.tool_name}({tc.arguments}) -> {tc.result}"
            for tc in result.tool_calls_made
        ]) if result.tool_calls_made else "No tool calls made"

        evaluation_prompt = f"""You are an expert judge evaluating the quality of an AI assistant's response to a user query.

## Original User Query
{original_query}

## Available Tools
{tool_descriptions}

## Tools Called by the Model
{tool_calls_summary}

## Model's Final Response
{result.final_response}

## Evaluation Criteria
Score the response on a scale of 0-100 based on:
1. **Completeness (25 points)**: Did it address all parts of the query?
2. **Tool Usage (25 points)**: Were appropriate tools called? Were they used efficiently?
3. **Clarity (25 points)**: Is the response well-organized and easy to understand?
4. **Actionability (25 points)**: Can the user act on the recommendations provided?

## Response Format
Respond with a JSON object containing:
- "overall_score": integer from 0 to 100
- "completeness_score": integer from 0 to 25
- "tool_usage_score": integer from 0 to 25
- "clarity_score": integer from 0 to 25
- "actionability_score": integer from 0 to 25
- "feedback": string with detailed evaluation feedback

Respond ONLY with the JSON object, no additional text."""

        try:
            response = self.client.responses.create(
                model=self.model_name,
                input=[
                    {
                        "role": "user",
                        "content": evaluation_prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent judging
            )

            # Extract the response text
            response_text = response.output_text

            # Parse JSON response
            evaluation = json.loads(response_text)

            result.judge_score = evaluation.get("overall_score", 0)

            # Build detailed feedback
            feedback_parts = [
                f"Overall Score: {evaluation.get('overall_score', 0)}/100",
                f"- Completeness: {evaluation.get('completeness_score', 0)}/25",
                f"- Tool Usage: {evaluation.get('tool_usage_score', 0)}/25",
                f"- Clarity: {evaluation.get('clarity_score', 0)}/25",
                f"- Actionability: {evaluation.get('actionability_score', 0)}/25",
                "",
                f"Feedback: {evaluation.get('feedback', 'No feedback provided')}"
            ]
            result.judge_evaluation = "\n".join(feedback_parts)

        except json.JSONDecodeError as e:
            result.judge_score = 0
            result.judge_evaluation = f"Failed to parse judge response: {e}"

        except Exception as e:
            result.judge_score = 0
            result.judge_evaluation = f"Judge evaluation failed: {e}"

        return result
