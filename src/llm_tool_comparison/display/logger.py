"""Display logger using Rich for beautiful terminal output."""

import json
from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown

from ..providers.base import ConversationResult, ToolCall


class ConversationLogger:
    """Logger for displaying conversation progress with Rich formatting."""

    def __init__(self):
        """Initialize the logger with a Rich console."""
        self.console = Console()

    def show_model_header(self, model_name: str):
        """Display a header for the model being tested.

        Args:
            model_name: Name of the model
        """
        self.console.rule(f"[bold cyan]Testing {model_name}[/bold cyan]", style="cyan")
        self.console.print()

    def show_user_message(self, message: str):
        """Display the user's query.

        Args:
            message: User's question/request
        """
        self.console.print(Panel(
            message,
            title="[bold blue]User Query[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        ))
        self.console.print()

    def show_tool_calls(self, tool_calls: List[ToolCall]):
        """Display tool calls made during the conversation.

        Args:
            tool_calls: List of ToolCall objects
        """
        if not tool_calls:
            return

        self.console.print("[bold yellow]Tool Calls:[/bold yellow]")

        for i, tc in enumerate(tool_calls, 1):
            # Create a table for this tool call
            table = Table(
                title=f"Tool {i}: {tc.tool_name}",
                show_header=True,
                header_style="bold yellow",
                border_style="yellow"
            )

            table.add_column("Parameter", style="cyan", width=20)
            table.add_column("Value", style="white")

            # Add arguments
            if isinstance(tc.arguments, dict):
                for key, value in tc.arguments.items():
                    table.add_row(key, str(value))
            else:
                # If arguments is a string (JSON), try to parse it
                try:
                    args_dict = json.loads(tc.arguments) if isinstance(tc.arguments, str) else tc.arguments
                    for key, value in args_dict.items():
                        table.add_row(key, str(value))
                except:
                    table.add_row("arguments", str(tc.arguments))

            self.console.print(table)

            # Show result if available
            if tc.result:
                result_str = str(tc.result)
                if len(result_str) > 500:
                    result_str = result_str[:500] + "..."

                self.console.print(Panel(
                    result_str,
                    title="[green]Result[/green]",
                    border_style="green",
                    padding=(0, 1)
                ))

            self.console.print()

    def show_final_response(self, response: str):
        """Display the final assistant response.

        Args:
            response: Final text response from the assistant
        """
        # Handle None or empty response
        if not response:
            response = "(No response content)"

        # Try to render as markdown for better formatting
        try:
            md = Markdown(response)
            self.console.print(Panel(
                md,
                title="[bold green]Assistant Response[/bold green]",
                border_style="green",
                padding=(1, 2)
            ))
        except:
            # Fallback to plain text
            self.console.print(Panel(
                str(response),
                title="[bold green]Assistant Response[/bold green]",
                border_style="green",
                padding=(1, 2)
            ))

        self.console.print()

    def show_summary(self, result: ConversationResult):
        """Display execution summary.

        Args:
            result: ConversationResult with metadata
        """
        table = Table(show_header=False, border_style="dim")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Model", result.model_name)
        table.add_row("Success", "✓" if result.success else "✗")
        table.add_row("Duration", f"{result.total_duration:.2f}s")
        table.add_row("Tool Calls", str(len(result.tool_calls_made)))

        if not result.success and result.error_message:
            table.add_row("Error", result.error_message)

        self.console.print(Panel(
            table,
            title="[bold]Execution Summary[/bold]",
            border_style="dim"
        ))
        self.console.print()

    def show_comparison_table(self, results: List[ConversationResult]):
        """Display a comparison table of all model results.

        Args:
            results: List of ConversationResult objects from all models
        """
        self.console.rule("[bold magenta]Comparison Summary[/bold magenta]", style="magenta")
        self.console.print()

        table = Table(
            show_header=True,
            header_style="bold magenta",
            border_style="magenta"
        )

        table.add_column("Model", style="cyan", width=20)
        table.add_column("Success", justify="center")
        table.add_column("Tool Calls", justify="right")
        table.add_column("Duration (s)", justify="right")
        table.add_column("Avg per Call (s)", justify="right")

        for result in results:
            success_icon = "✓" if result.success else "✗"
            success_style = "green" if result.success else "red"

            tool_count = len(result.tool_calls_made)
            avg_time = result.total_duration / max(tool_count, 1)

            table.add_row(
                result.model_name,
                f"[{success_style}]{success_icon}[/{success_style}]",
                str(tool_count),
                f"{result.total_duration:.2f}",
                f"{avg_time:.2f}"
            )

        self.console.print(table)
        self.console.print()

    def show_error(self, message: str):
        """Display an error message.

        Args:
            message: Error message to display
        """
        self.console.print(Panel(
            f"[bold red]Error:[/bold red] {message}",
            border_style="red"
        ))
        self.console.print()
