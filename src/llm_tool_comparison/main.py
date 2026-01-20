"""Main CLI entry point for LLM Tool Calling Comparison System."""

import typer
from typing import List
from langfuse import Langfuse
from openinference.instrumentation.haystack import HaystackInstrumentor

from .config.settings import settings
from .providers.openai_provider import OpenAIProvider
from .providers.google_provider import GoogleProvider
from .display.logger import ConversationLogger
from .scenarios.travel import TRAVEL_QUERY, TRAVEL_SCENARIO_DESCRIPTION

app = typer.Typer(
    name="llm-tool-comparison",
    help="Compare tool calling abilities of different LLM models"
)

# Initialize LangFuse instrumentation at module level if enabled
# This will automatically trace all Haystack operations
if settings.langfuse_enabled:
    HaystackInstrumentor().instrument()


@app.command()
def compare(
    models: List[str] = typer.Option(
        ["gpt-4.1", "gpt-5.2", "gemini-3-flash", "gemini-3-pro"],
        "--model",
        "-m",
        help="Models to compare (can be specified multiple times)"
    ),
    show_scenario: bool = typer.Option(
        False,
        "--show-scenario",
        "-s",
        help="Show scenario description before running"
    )
):
    """Compare tool calling across different LLM models.

    This command runs the Travel Research Assistant scenario with each
    specified model and displays formatted results with tool calls and
    final responses.

    Example:
        llm-tool-comparison compare -m gpt-4.1 -m gemini-3-flash
    """
    logger = ConversationLogger()

    # Initialize LangFuse client if enabled
    langfuse = None
    if settings.langfuse_enabled:
        try:
            langfuse = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_base_url,
                environment="unit-test-silvan"
            )

            # Verify connection
            langfuse.auth_check()
            logger.console.print("[dim]✓ LangFuse connection verified[/dim]\n")

        except Exception as e:
            logger.show_error(f"Failed to connect to LangFuse: {e}")
            logger.console.print("[yellow]Continuing without LangFuse tracing...[/yellow]\n")
            langfuse = None

    # Show scenario description if requested
    if show_scenario:
        logger.console.print(TRAVEL_SCENARIO_DESCRIPTION)
        logger.console.print()

    results = []

    # Process each model
    for model_name in models:
        try:
            # Create provider based on model name
            if model_name.startswith("gpt"):
                provider = OpenAIProvider(model_name)
            elif model_name.startswith("gemini"):
                provider = GoogleProvider(model_name)
            else:
                logger.show_error(f"Unknown model type: {model_name}")
                continue

            # Display header
            logger.show_model_header(model_name)
            logger.show_user_message(TRAVEL_QUERY)

            # Run conversation
            result = provider.run_conversation(TRAVEL_QUERY)

            # Display results
            logger.show_tool_calls(result.tool_calls_made)
            logger.show_final_response(result.final_response)
            logger.show_summary(result)

            results.append(result)

        except Exception as e:
            logger.show_error(f"Error testing {model_name}: {str(e)}")
            import traceback
            logger.console.print(f"[dim]{traceback.format_exc()}[/dim]")

    # Ensure traces are sent to LangFuse
    if langfuse:
        try:
            langfuse.flush()
            logger.console.print("[dim]✓ Traces sent to LangFuse[/dim]\n")
        except Exception as e:
            logger.console.print(f"[yellow]Warning: Failed to flush to LangFuse: {e}[/yellow]\n")

    # Show comparison table if we have multiple results
    if len(results) > 1:
        logger.show_comparison_table(results)

    # Summary message
    logger.console.print("[bold green]✓ Comparison complete![/bold green]")

    if langfuse:
        logger.console.print(f"\n[dim]View traces at: {settings.langfuse_base_url}[/dim]")


@app.command()
def info():
    """Show information about available models and tools."""
    logger = ConversationLogger()

    logger.console.rule("[bold]Available Models[/bold]")
    logger.console.print()

    models_info = [
        ("gpt-4.1", "OpenAI GPT-4.1", "High performance, general purpose"),
        ("gpt-5.2", "OpenAI GPT-5.2", "Latest GPT model"),
        ("gemini-3-flash", "Google Gemini 2.0 Flash", "Fast, efficient"),
        ("gemini-3-pro", "Google Gemini 2.0 Pro", "High quality responses"),
    ]

    for model_id, display_name, description in models_info:
        logger.console.print(f"[cyan]{model_id:20}[/cyan] {display_name:30} - {description}")

    logger.console.print()
    logger.console.rule("[bold]Available Tools[/bold]")
    logger.console.print()

    tools_info = [
        ("get_weather_forecast", "Get weather forecast for a location and month"),
        ("search_hotels", "Search for hotels in a city/area with price filtering"),
        ("find_attractions", "Find tourist attractions in a city"),
        ("convert_currency", "Convert between currencies"),
        ("get_transportation_info", "Get transportation information for a city"),
    ]

    for tool_name, description in tools_info:
        logger.console.print(f"[yellow]{tool_name:25}[/yellow] {description}")

    logger.console.print()


@app.command()
def test_connection():
    """Test connections to OpenAI, Google, and LangFuse."""
    logger = ConversationLogger()

    logger.console.rule("[bold]Testing Connections[/bold]")
    logger.console.print()

    # Test LangFuse (if enabled)
    if settings.langfuse_enabled:
        try:
            langfuse = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_base_url,
                environment="unit-test-silvan"
            )
            langfuse.auth_check()
            logger.console.print("[green]✓ LangFuse connection successful[/green]")
        except Exception as e:
            logger.console.print(f"[red]✗ LangFuse connection failed: {e}[/red]")
    else:
        logger.console.print("[dim]⊝ LangFuse disabled (set LANGFUSE_ENABLED=true to enable)[/dim]")

    # Test OpenAI (with a simple API key check)
    try:
        if settings.openai_api_key and settings.openai_api_key.startswith("sk-"):
            logger.console.print("[green]✓ OpenAI API key present[/green]")
        else:
            logger.console.print("[yellow]⚠ OpenAI API key format looks incorrect[/yellow]")
    except Exception as e:
        logger.console.print(f"[red]✗ OpenAI API key check failed: {e}[/red]")

    # Test Google API key
    try:
        if settings.google_api_key and len(settings.google_api_key) > 10:
            logger.console.print("[green]✓ Google API key present[/green]")
        else:
            logger.console.print("[yellow]⚠ Google API key format looks incorrect[/yellow]")
    except Exception as e:
        logger.console.print(f"[red]✗ Google API key check failed: {e}[/red]")

    logger.console.print()


if __name__ == "__main__":
    app()
