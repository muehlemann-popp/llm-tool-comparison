"""Google Gemini model provider implementation using native google-genai SDK."""

import time
from typing import List
from google import genai
from google.genai import types

from .base import ModelProvider, ConversationResult, ToolCall
from ..config.settings import settings
from ..tools import get_all_tools


class GoogleNativeProvider(ModelProvider):
    """Provider for Google Gemini models using the native google-genai SDK."""

    def __init__(self, model_name: str):
        """Initialize Google provider.

        Args:
            model_name: Gemini model name (e.g., "gemini-native-flash", "gemini-native-pro")
        """
        self.model_name = model_name
        self.tools = get_all_tools()
        self.client = genai.Client(api_key=settings.google_api_key)
        self._tool_functions = self._build_tool_functions()
        self._tool_declarations = self._build_tool_declarations()

    def _build_tool_functions(self) -> dict:
        """Build a mapping of tool names to their functions."""
        return {tool.name: tool.function for tool in self.tools}

    def _build_tool_declarations(self) -> types.Tool:
        """Build tool declarations for the Gemini API."""
        function_declarations = []
        for tool in self.tools:
            func_decl = types.FunctionDeclaration(
                name=tool.name,
                description=tool.description,
                parameters=tool.parameters
            )
            function_declarations.append(func_decl)
        return types.Tool(function_declarations=function_declarations)

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
        tool_calls_made: List[ToolCall] = []

        # Map friendly names to actual model names
        model_mapping = {
            "gemini-native-flash": "gemini-3-flash-preview",
            "gemini-native-pro": "gemini-3-pro-preview",
        }
        actual_model = model_mapping.get(self.model_name, self.model_name)

        max_iterations = 10
        iteration = 0

        # Build contents for conversation
        contents = [
            types.Content(
                role='user',
                parts=[types.Part.from_text(text=query)]
            )
        ]

        try:
            while iteration < max_iterations:
                iteration += 1

                # Generate content with tools
                response = self.client.models.generate_content(
                    model=actual_model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        tools=[self._tool_declarations],
                        temperature=0.7,
                    ),
                )

                # Check if there are function calls
                if response.function_calls:
                    # Process each function call
                    function_response_parts = []

                    for fc in response.function_calls:
                        tool_name = fc.name
                        args = dict(fc.args) if fc.args else {}

                        # Record the tool call
                        tool_calls_made.append(ToolCall(
                            tool_name=tool_name,
                            arguments=args,
                            result=None
                        ))

                        # Execute the tool
                        if tool_name in self._tool_functions:
                            try:
                                result = self._tool_functions[tool_name](**args)
                                tool_calls_made[-1].result = result
                            except Exception as e:
                                result = f"Error executing tool: {str(e)}"
                                tool_calls_made[-1].result = result
                        else:
                            result = f"Unknown tool: {tool_name}"
                            tool_calls_made[-1].result = result

                        # Build function response part
                        function_response_parts.append(
                            types.Part.from_function_response(
                                name=tool_name,
                                response={'result': result}
                            )
                        )

                    # Add model's response and tool results to conversation
                    contents.append(response.candidates[0].content)
                    contents.append(
                        types.Content(
                            role='user',
                            parts=function_response_parts
                        )
                    )

                else:
                    # No function calls - conversation complete
                    final_response = response.text if response.text else ""

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
