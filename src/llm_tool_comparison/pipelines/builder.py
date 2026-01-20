"""Pipeline builder for tool-calling workflows."""

from dataclasses import dataclass
from haystack import Pipeline
from haystack.components.tools import ToolInvoker
from haystack.dataclasses import ChatMessage
from typing import List, Any


@dataclass
class ToolCallingComponents:
    """Container for tool calling components."""
    pipeline: Pipeline
    tool_invoker: ToolInvoker


def build_tool_calling_pipeline(chat_generator: Any, tools: List[Any]) -> ToolCallingComponents:
    """Build tool-calling components.

    This builds a minimal pipeline with just a generator, and a separate tool invoker.
    The calling code handles the conversation loop and decides when to invoke tools.

    Args:
        chat_generator: Haystack chat generator component (OpenAI or Google)
        tools: List of tool instances to make available

    Returns:
        ToolCallingComponents with pipeline and tool_invoker
    """
    pipeline = Pipeline()

    # Add the chat generator
    pipeline.add_component("generator", chat_generator)

    # Tool invoker executes tools (kept separate for direct invocation)
    tool_invoker = ToolInvoker(tools=tools)

    return ToolCallingComponents(pipeline=pipeline, tool_invoker=tool_invoker)


def has_tool_calls(message: ChatMessage) -> bool:
    """Check if a ChatMessage contains tool calls.

    Args:
        message: The ChatMessage to check

    Returns:
        True if the message contains tool calls
    """
    # Check for tool calls in _content (Haystack's newer format)
    if hasattr(message, '_content') and message._content:
        for item in message._content:
            # Check if item is a ToolCall object (has tool_name attribute)
            if hasattr(item, 'tool_name'):
                return True

    # Also check meta for backwards compatibility
    if hasattr(message, 'meta') and message.meta:
        tool_calls = message.meta.get('tool_calls', [])
        if tool_calls:
            return True

    return False


def get_tool_calls_from_message(message: ChatMessage) -> list:
    """Extract tool calls from a ChatMessage.

    Args:
        message: The ChatMessage to extract tool calls from

    Returns:
        List of tool call objects
    """
    tool_calls = []

    # Check for tool calls in _content (Haystack's newer format)
    if hasattr(message, '_content') and message._content:
        for item in message._content:
            if hasattr(item, 'tool_name'):
                tool_calls.append(item)

    return tool_calls


def extract_text_content(message: ChatMessage) -> str:
    """Extract text content from a ChatMessage.

    Handles different content formats in Haystack ChatMessage.

    Args:
        message: The ChatMessage to extract text from

    Returns:
        The text content as a string (never None)
    """
    if message is None:
        return ""

    # Check for _content attribute (list of content objects)
    if hasattr(message, '_content') and message._content:
        texts = []
        for content in message._content:
            if hasattr(content, 'text') and content.text:
                texts.append(content.text)
        if texts:
            return '\n'.join(texts)

    # Check for content attribute (direct string or property)
    if hasattr(message, 'content'):
        content = message.content
        if content is None:
            pass  # Continue checking other attributes
        elif isinstance(content, str):
            return content
        elif isinstance(content, list):
            texts = []
            for item in content:
                if hasattr(item, 'text') and item.text:
                    texts.append(item.text)
                elif isinstance(item, str):
                    texts.append(item)
            if texts:
                return '\n'.join(texts)

    # Check for text attribute directly
    if hasattr(message, 'text') and message.text:
        return message.text

    # Last resort: convert to string
    result = str(message)
    if result and result != 'None':
        return result

    return ""
