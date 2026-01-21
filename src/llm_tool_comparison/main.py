"""Main CLI entry point for LLM Tool Calling Comparison System."""

import typer
from typing import List
from langfuse import Langfuse
from openinference.instrumentation.haystack import HaystackInstrumentor

from .config.settings import settings
from .providers.openai_provider import OpenAIProvider
from .providers.google_native_provider import GoogleNativeProvider
from .providers.google_haystack_provider import GoogleHaystackProvider
from .providers.google_agent_provider import GoogleAgentProvider
from .providers.judge_provider import JudgeProvider
from .display.logger import ConversationLogger
from .scenarios import get_scenario, list_scenarios, DEFAULT_SCENARIO
from .tools import get_all_tools

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
        ["gpt-4.1", "gemini-native-flash", "gemini-haystack-flash", "gemini-agent-flash"],
        "--model",
        "-m",
        help="Models to compare. Gemini variants: gemini-native-*, gemini-haystack-*, gemini-agent-* (flash/pro)"
    ),
    scenario: str = typer.Option(
        DEFAULT_SCENARIO,
        "--scenario",
        "-S",
        help="Scenario to run (travel, simple)"
    ),
    show_scenario: bool = typer.Option(
        False,
        "--show-scenario",
        "-s",
        help="Show scenario description before running"
    )
):
    """Compare tool calling across different LLM models.

    This command runs a scenario with each specified model and displays
    formatted results with tool calls and final responses.

    Example:
        llm-tool-comparison compare -m gpt-4.1 -S simple
    """
    logger = ConversationLogger()

    # Get the scenario
    try:
        current_scenario = get_scenario(scenario)
    except ValueError as e:
        logger.show_error(str(e))
        raise typer.Exit(1)

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
        logger.console.print(current_scenario.description)
        logger.console.print()

    results = []

    # Process each model
    for model_name in models:
        try:
            # Create provider based on model name
            if model_name.startswith("gpt"):
                provider = OpenAIProvider(model_name)
            elif model_name.startswith("gemini-native"):
                provider = GoogleNativeProvider(model_name)
            elif model_name.startswith("gemini-haystack"):
                provider = GoogleHaystackProvider(model_name)
            elif model_name.startswith("gemini-agent"):
                provider = GoogleAgentProvider(model_name)
            else:
                logger.show_error(f"Unknown model type: {model_name}. Use gemini-native-* or gemini-haystack-* for Gemini models.")
                continue

            # Display header
            logger.show_model_header(model_name)
            logger.show_user_message(current_scenario.query)

            # Run conversation
            result = provider.run_conversation(
                current_scenario.query,
                system_prompt=current_scenario.system_prompt
            )

            # Judge evaluation
            if settings.judge_enabled and result.success:
                judge = JudgeProvider(model_name=settings.judge_model)
                result = judge.evaluate_response(
                    result,
                    current_scenario.query,
                    get_all_tools()
                )

            # Display results
            logger.show_tool_calls(result.tool_calls_made)
            logger.show_final_response(result.final_response)
            logger.show_summary(result)

            # Show judge evaluation if available
            if result.judge_evaluation:
                logger.show_judge_evaluation(result)

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
        ("gemini-native-flash", "Gemini 3 Flash (native)", "Native google-genai SDK"),
        ("gemini-native-pro", "Gemini 3 Pro (native)", "Native google-genai SDK"),
        ("gemini-haystack-flash", "Gemini 3 Flash (Haystack)", "Via Haystack integration"),
        ("gemini-haystack-pro", "Gemini 3 Pro (Haystack)", "Via Haystack integration"),
        ("gemini-agent-flash", "Gemini 3 Flash (Agent)", "Via Haystack Agent component"),
        ("gemini-agent-pro", "Gemini 3 Pro (Agent)", "Via Haystack Agent component"),
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
