"""Google Gemini provider using Haystack Agent component."""

import time
from typing import List
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret
from haystack_integrations.components.generators.google_genai import GoogleGenAIChatGenerator

from .base import ModelProvider, ConversationResult, ToolCall
from ..config.settings import settings
from ..tools import get_all_tools


class GoogleAgentProvider(ModelProvider):
    """Provider using Haystack's Agent for automatic tool loop."""

    def __init__(self, model_name: str):
        """Initialize Google Agent provider.

        Args:
            model_name: Gemini model name (e.g., "gemini-agent-flash", "gemini-agent-pro")
        """
        self.model_name = model_name
        self.tools = get_all_tools()

        # Map friendly names to actual model names
        model_mapping = {
            "gemini-agent-flash": "gemini-3-flash-preview",
            "gemini-agent-pro": "gemini-3-pro-preview",
        }
        actual_model = model_mapping.get(model_name, model_name)

        generator = GoogleGenAIChatGenerator(
            api_key=Secret.from_token(settings.google_api_key),
            model=actual_model,
            generation_kwargs={"temperature": 0.7},
        )

        self.agent = Agent(
            chat_generator=generator,
            tools=self.tools,
            max_agent_steps=10,
            raise_on_tool_invocation_failure=False,
        )
        self.agent.warm_up()

    def get_model_name(self) -> str:
        """Get the model name."""
        return self.model_name

    def run_conversation(self, query: str, system_prompt: str = "") -> ConversationResult:
        """Run conversation with tool calling using Haystack Agent.

        Args:
            query: User's question
            system_prompt: Optional system prompt to set context

        Returns:
            ConversationResult with final response and metadata
        """
        start_time = time.time()
        tool_calls_made: List[ToolCall] = []

        try:
            messages = []
            if system_prompt:
                messages.append(ChatMessage.from_system(system_prompt))
            messages.append(ChatMessage.from_user(query))
            result = self.agent.run(messages=messages)
            messages = result.get("messages", [])

            # Extract tool calls from all messages
            for msg in messages:
                # Extract tool calls from message
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_calls_made.append(ToolCall(
                            tool_name=getattr(tc, 'tool_name', 'unknown'),
                            arguments=getattr(tc, 'arguments', {}) or {},
                            result=None
                        ))

                # Try to get tool results from tool_call_results
                if hasattr(msg, 'tool_call_results') and msg.tool_call_results:
                    for tcr in msg.tool_call_results:
                        # Match result to last tool call with same name
                        origin = getattr(tcr, 'origin', None)
                        if origin:
                            origin_name = getattr(origin, 'tool_name', None)
                            for tc_made in reversed(tool_calls_made):
                                if tc_made.tool_name == origin_name and tc_made.result is None:
                                    tc_made.result = getattr(tcr, 'result', str(tcr))
                                    break

            # Final response is last message text
            final_response = ""
            if messages:
                last_msg = messages[-1]
                if hasattr(last_msg, 'text'):
                    final_response = last_msg.text or ""
                elif hasattr(last_msg, 'content'):
                    final_response = last_msg.content or ""

            return ConversationResult(
                model_name=self.model_name,
                final_response=final_response,
                tool_calls_made=tool_calls_made,
                total_duration=time.time() - start_time,
                success=True
            )
        except Exception as e:
            return ConversationResult(
                model_name=self.model_name,
                final_response=f"Error: {str(e)}",
                tool_calls_made=tool_calls_made,
                total_duration=time.time() - start_time,
                success=False,
                error_message=str(e)
            )
