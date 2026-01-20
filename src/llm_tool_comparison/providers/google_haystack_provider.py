"""Google Gemini model provider implementation using Haystack integration."""

import time
from typing import List
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret
from haystack_integrations.components.generators.google_genai import GoogleGenAIChatGenerator

from .base import ModelProvider, ConversationResult, ToolCall
from ..config.settings import settings
from ..pipelines.builder import build_tool_calling_pipeline, has_tool_calls, extract_text_content, get_tool_calls_from_message
from ..tools import get_all_tools


class GoogleHaystackProvider(ModelProvider):
    """Provider for Google Gemini models using Haystack integration."""

    def __init__(self, model_name: str):
        """Initialize Google Haystack provider.

        Args:
            model_name: Gemini model name (e.g., "gemini-haystack-flash", "gemini-haystack-pro")
        """
        self.model_name = model_name
        self.tools = get_all_tools()
        components = self._create_pipeline()
        self.pipeline = components.pipeline
        self.tool_invoker = components.tool_invoker

    def _create_pipeline(self):
        """Create Haystack pipeline with Google Gemini generator and tools."""
        # Map friendly names to actual model names
        model_mapping = {
            "gemini-haystack-flash": "gemini-3-flash-preview",
            "gemini-haystack-pro": "gemini-3-pro-preview",
        }
        actual_model = model_mapping.get(self.model_name, self.model_name)

        generator = GoogleGenAIChatGenerator(
            api_key=Secret.from_token(settings.google_api_key),
            model=actual_model,
            generation_kwargs={"temperature": 0.7},
            tools=self.tools,
        )

        return build_tool_calling_pipeline(generator, self.tools)

    def get_model_name(self) -> str:
        """Get the model name."""
        return self.model_name

    def run_conversation(self, query: str) -> ConversationResult:
        """Run conversation with tool calling.

        Args:
            query: User's question

        Returns:
            ConversationResult with final response and metadata
        """
        start_time = time.time()
        messages = [ChatMessage.from_user(query)]
        tool_calls_made: List[ToolCall] = []

        max_iterations = 10
        iteration = 0

        try:
            while iteration < max_iterations:
                iteration += 1

                # Run generator only
                result = self.pipeline.run({"generator": {"messages": messages}})

                # Get the reply from generator
                replies = result.get("generator", {}).get("replies", [])
                if not replies:
                    return ConversationResult(
                        model_name=self.model_name,
                        final_response="No response from generator",
                        tool_calls_made=tool_calls_made,
                        total_duration=time.time() - start_time,
                        success=False,
                        error_message="Empty replies from generator"
                    )

                reply = replies[0]

                # Check if tool calls were made
                if has_tool_calls(reply):
                    # Extract tool calls from the reply
                    for tc in get_tool_calls_from_message(reply):
                        tool_calls_made.append(ToolCall(
                            tool_name=getattr(tc, 'tool_name', 'unknown'),
                            arguments=getattr(tc, 'arguments', {}),
                            result=None
                        ))

                    # Add assistant message to conversation
                    messages.append(reply)

                    # Run tool invoker directly
                    tool_result = self.tool_invoker.run(messages=[reply])
                    tool_messages = tool_result.get("tool_messages", [])

                    # Add tool results to conversation
                    messages.extend(tool_messages)

                    # Update tool call results
                    for i, tool_msg in enumerate(tool_messages):
                        if i < len(tool_calls_made) - len(tool_messages) + i + 1:
                            idx = len(tool_calls_made) - len(tool_messages) + i
                            if idx >= 0 and idx < len(tool_calls_made):
                                tool_calls_made[idx].result = extract_text_content(tool_msg)

                else:
                    # No tools called - conversation complete
                    final_response = extract_text_content(reply)

                    return ConversationResult(
                        model_name=self.model_name,
                        final_response=final_response,
                        tool_calls_made=tool_calls_made,
                        total_duration=time.time() - start_time,
                        success=True
                    )

            # Max iterations reached
            return ConversationResult(
                model_name=self.model_name,
                final_response="Max iterations reached without completion",
                tool_calls_made=tool_calls_made,
                total_duration=time.time() - start_time,
                success=False,
                error_message=f"Exceeded {max_iterations} iterations"
            )

        except Exception as e:
            return ConversationResult(
                model_name=self.model_name,
                final_response=f"Error during conversation: {str(e)}",
                tool_calls_made=tool_calls_made,
                total_duration=time.time() - start_time,
                success=False,
                error_message=str(e)
            )
