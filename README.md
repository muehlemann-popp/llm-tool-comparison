# LLM Tool Calling Comparison System

A Python application to test and compare tool calling abilities of modern LLM models using Haystack for orchestration and LangFuse for observability.

## Overview

This system tests how different LLM models handle function calling / tool use by running various scenarios that require multiple tool calls. It includes a GPT-4.1 judge to evaluate response quality, and displays formatted terminal output showing the dialogue, tool executions, and final responses for easy comparison.

### Supported Models

| Model ID | Provider | Description |
|----------|----------|-------------|
| `gpt-4.1` | OpenAI | GPT-4.1 via Haystack |
| `gpt-5.2` | OpenAI | GPT-5.2 via Haystack |
| `gemini-native-flash` | Google | Gemini 3 Flash via native SDK |
| `gemini-native-pro` | Google | Gemini 3 Pro via native SDK |
| `gemini-haystack-flash` | Google | Gemini 3 Flash via Haystack |
| `gemini-haystack-pro` | Google | Gemini 3 Pro via Haystack |
| `gemini-agent-flash` | Google | Gemini 3 Flash via Haystack Agent |
| `gemini-agent-pro` | Google | Gemini 3 Pro via Haystack Agent |

### Available Tools

The system provides 16 mock tools with realistic data:

**Travel Tools:**
- `get_weather_forecast` - Weather information for a location and month
- `search_hotels` - Find hotels with price filtering
- `find_attractions` - Discover tourist attractions
- `convert_currency` - Currency conversion
- `get_transportation_info` - Airport and transport details

**Hapimag Resort Tools:**
- `hapimag_get_resort_details` - Resort information
- `hapimag_get_resort_apartments` - Available apartments
- `hapimag_get_charging_station_for_resort` - EV charging info
- `hapimag_get_resort_gastronomy_details` - Dining options
- `hapimag_get_activities_overview` - Activities list
- `hapimag_get_activities_details` - Activity details
- `hapimag_get_resort_services` - Resort services
- `hapimag_get_pet_charge` - Pet policy and charges

**Maps & Weather Tools:**
- `maps_search_nearby_places` - Search nearby places
- `maps_get_places_details` - Place details
- `owm_daily_forecast` - OpenWeatherMap daily forecast

### Available Scenarios

| Scenario | Description |
|----------|-------------|
| `travel` | Travel planning to Tokyo (default) |
| `simple` | Basic tool calling test |
| `resort` | Hapimag resort amenities query with system prompt |

## Architecture

```
Tech Stack:
├── Haystack         - LLM orchestration and tool calling
├── google-genai     - Native Google Gemini SDK
├── LangFuse         - Observability and tracing
├── Typer            - CLI interface
├── Rich             - Terminal formatting
└── Pydantic         - Settings management

Project Structure:
src/llm_tool_comparison/
├── config/          - Configuration and settings
├── tools/           - Mock tool implementations
│   ├── weather.py, hotels.py, ...  (travel tools)
│   ├── hapimag.py   (resort tools)
│   ├── maps.py      (maps tools)
│   └── openweathermap.py
├── providers/
│   ├── base.py                    - ModelProvider ABC
│   ├── openai_provider.py         - OpenAI via Haystack
│   ├── google_native_provider.py  - Gemini via native SDK
│   ├── google_haystack_provider.py - Gemini via Haystack
│   ├── google_agent_provider.py   - Gemini via Haystack Agent
│   └── judge_provider.py          - GPT-4.1 judge
├── pipelines/       - Reusable pipeline builder
├── display/         - Rich terminal formatting
└── scenarios/       - Test scenarios with system prompts
```

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- [Task](https://taskfile.dev/) (optional, for task automation)
- API keys for OpenAI, Google AI, and LangFuse

### Setup

```bash
# Clone the repository
git clone https://github.com/muehlemann-popp/llm-tool-comparison.git
cd llm-tool-comparison

# Run setup
task setup

# Or manually:
uv venv
source .venv/bin/activate.fish  # or activate.sh for bash
uv pip install -e .
cp .env.example .env
```

Configure `.env` with your API keys:

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
JUDGE_ENABLED=true
JUDGE_MODEL=gpt-4.1
```

## Usage

### Run Comparison

```bash
# Compare default models with travel scenario
uv run python -m src.llm_tool_comparison.main compare

# Compare specific models
uv run python -m src.llm_tool_comparison.main compare -m gemini-native-pro -m gpt-4.1

# Run resort scenario
uv run python -m src.llm_tool_comparison.main compare -m gemini-native-pro -S resort

# Show scenario description
uv run python -m src.llm_tool_comparison.main compare -S resort --show-scenario
```

### Other Commands

```bash
# View available models and tools
uv run python -m src.llm_tool_comparison.main info

# Test API connections
uv run python -m src.llm_tool_comparison.main test-connection
```

## Output

The system provides rich terminal output including:

- **Model Header** - Shows which model is being tested
- **User Query Panel** - Displays the original question
- **Tool Calls Tables** - Shows each tool call with parameters and results
- **Final Response** - The assistant's synthesized answer (Markdown)
- **Execution Summary** - Duration, success status, tool count
- **Judge Evaluation** - Quality score (0-100) with detailed feedback
- **Comparison Table** - Side-by-side comparison of all models

## Judge Evaluation

When enabled, responses are evaluated by GPT-4.1 on four criteria:
- **Completeness** (25 pts) - All aspects of the query addressed
- **Tool Usage** (25 pts) - Appropriate and efficient tool use
- **Clarity** (25 pts) - Clear and well-organized response
- **Actionability** (25 pts) - Practical, actionable information

## LangFuse Integration

All operations are automatically traced to LangFuse:
- Tool invocations and results
- LLM generations and responses
- Performance metrics and durations

View traces at: https://cloud.langfuse.com

## Development

### Adding New Tools

1. Create a tool file in `src/llm_tool_comparison/tools/`
2. Define the function and create a Haystack `Tool`
3. Export in `tools/__init__.py`

```python
from haystack.tools import Tool

def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result for {param}"

my_tool_def = Tool(
    name="my_tool",
    description="Does something useful",
    function=my_tool,
    parameters={
        "type": "object",
        "properties": {"param": {"type": "string"}},
        "required": ["param"]
    }
)
```

### Adding New Scenarios

1. Create a scenario file in `src/llm_tool_comparison/scenarios/`
2. Register in `scenarios/registry.py`

```python
# scenarios/my_scenario.py
MY_QUERY = "User question here"
MY_DESCRIPTION = "Scenario description"
MY_SYSTEM_PROMPT = "Optional system prompt"
```

### Adding New Providers

1. Create a provider in `src/llm_tool_comparison/providers/`
2. Inherit from `ModelProvider`
3. Implement `get_model_name()` and `run_conversation(query, system_prompt)`

## License

MIT License

## Contributing

Contributions welcome! Please fork, create a feature branch, and submit a PR.
