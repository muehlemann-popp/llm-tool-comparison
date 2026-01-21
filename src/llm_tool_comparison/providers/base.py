"""Base provider abstract class defining the interface for LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ToolCall:
    """Represents a single tool call made by the LLM."""

    tool_name: str
    arguments: Dict[str, Any]
    result: Any = None


@dataclass
class ConversationResult:
    """Result of a conversation with tool calling.

    Attributes:
        model_name: Name of the model used
        final_response: Final text response from the assistant
        tool_calls_made: List of all tool calls during the conversation
        total_duration: Total time taken in seconds
        success: Whether the conversation completed successfully
        error_message: Error message if success is False
        judge_score: Overall quality score from judge (0-100)
        judge_evaluation: Detailed feedback from judge
    """

    model_name: str
    final_response: str
    tool_calls_made: List[ToolCall] = field(default_factory=list)
    total_duration: float = 0.0
    success: bool = True
    error_message: str = ""
    judge_score: float = 0.0
    judge_evaluation: str = ""


class ModelProvider(ABC):
    """Abstract base class for LLM model providers.

    Subclasses must implement methods to:
    - Return the model name
    - Run a conversation with tool calling enabled
    """

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the name of the model.

        Returns:
            Model name string (e.g., "gpt-4.1", "gemini-3-flash")
        """
        pass

    @abstractmethod
    def run_conversation(self, query: str, system_prompt: str = "") -> ConversationResult:
        """Run a conversation with the user query.

        The implementation should:
        1. Send the query to the LLM (with optional system prompt)
        2. Handle any tool calls iteratively
        3. Return the final result with metadata

        Args:
            query: User's question/request
            system_prompt: Optional system prompt to set context

        Returns:
            ConversationResult with response and metadata
        """
        pass
