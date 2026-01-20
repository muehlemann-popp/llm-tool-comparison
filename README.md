# LLM Tool Calling Comparison System

A Python application to test and compare tool calling abilities of modern LLM models using Haystack for orchestration and LangFuse for observability.

## Overview

This system tests how different LLM models handle function calling / tool use by running a **Travel Research Assistant** scenario that requires multiple tool calls. The application displays formatted terminal output showing the dialogue, tool executions, and final responses for easy comparison.

### Tested Models

- **GPT-4.1** (OpenAI)
- **GPT-5.2** (OpenAI)
- **Gemini 3 Flash** (Google Gemini 2.0 Flash)
- **Gemini 3 Pro** (Google Gemini 2.0 Pro)

### Available Tools

The system provides 5 mock tools with realistic data:

1. **Weather Forecast** - Get weather information for a location and month
2. **Hotel Search** - Find hotels with price filtering and area preferences
3. **Attractions Finder** - Discover tourist attractions by category
4. **Currency Converter** - Convert between different currencies
5. **Transportation Info** - Get airport and local transportation details

## Architecture

```
Tech Stack:
├── Haystack         - LLM orchestration and tool calling
├── LangFuse         - Observability and tracing (via OpenInference)
├── Typer            - CLI interface
├── Rich             - Terminal formatting and display
└── Pydantic         - Settings management

Project Structure:
├── src/llm_tool_comparison/
│   ├── config/          - Configuration and settings
│   ├── tools/           - Mock tool implementations
│   ├── providers/       - Model provider implementations
│   ├── pipelines/       - Reusable pipeline builder
│   ├── display/         - Rich terminal formatting
│   └── scenarios/       - Test scenarios
```

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- API keys for:
  - OpenAI
  - Google AI (Gemini)
  - LangFuse (for observability)

### Setup

1. **Clone or navigate to the project directory**

2. **Run the setup task**

```bash
task setup
```

This will:
- Create a virtual environment
- Install dependencies
- Copy `.env.example` to `.env`

3. **Configure environment variables**

Edit `.env` and add your API keys:

```bash
# LangFuse
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=https://cloud.langfuse.com

# OpenAI
OPENAI_API_KEY=sk-...

# Google Gemini
GOOGLE_API_KEY=...
```

4. **Test connections**

```bash
source .venv/bin/activate.fish
python -m llm_tool_comparison.main test-connection
```

## Usage

### Run Comparison

Compare all models with the default Travel Research Assistant scenario:

```bash
task run
```

Or activate the virtual environment and run directly:

```bash
source .venv/bin/activate.fish
python -m llm_tool_comparison.main compare
```

### Select Specific Models

Compare only specific models:

```bash
python -m llm_tool_comparison.main compare -m gpt-4.1 -m gemini-3-flash
```

### Show Scenario Details

Display the scenario description before running:

```bash
python -m llm_tool_comparison.main compare --show-scenario
```

### View Available Models and Tools

```bash
python -m llm_tool_comparison.main info
```

## Test Scenario: Travel Research Assistant

**User Query:**
> "I'm planning a 5-day trip to Tokyo in April. Can you help me plan this? I need to know the weather, find good hotels under $200/night near Shibuya, and suggest a 3-day itinerary."

**Expected Behavior:**
The model should:
1. Call `get_weather_forecast` for Tokyo in April
2. Call `search_hotels` for Shibuya area under $200
3. Call `find_attractions` for Tokyo
4. Optionally call `convert_currency` for USD to JPY
5. Optionally call `get_transportation_info` for Tokyo
6. Synthesize all information into a coherent travel plan

## Output

The system provides rich terminal output including:

- **Model Header** - Clearly shows which model is being tested
- **User Query Panel** - Displays the original question
- **Tool Calls Tables** - Shows each tool call with parameters
- **Tool Results** - Displays the data returned by each tool
- **Final Response** - The assistant's synthesized answer (rendered as Markdown)
- **Execution Summary** - Duration, success status, tool count
- **Comparison Table** - Side-by-side comparison of all models

## LangFuse Integration

All pipeline operations are automatically traced to LangFuse using OpenInference instrumentation:

- **Automatic Tracing** - No manual instrumentation needed
- **Tool Call Tracking** - All tool invocations are logged
- **LLM Generations** - Model interactions are captured
- **Performance Metrics** - Duration and success rates tracked

View traces at: https://cloud.langfuse.com

## Development

### Project Structure

```
260120_gemini_tool_calling/
├── src/llm_tool_comparison/
│   ├── config/
│   │   └── settings.py              # Pydantic settings
│   ├── tools/
│   │   ├── weather.py               # Weather tool + mock data
│   │   ├── hotels.py                # Hotel search tool
│   │   ├── attractions.py           # Attractions finder
│   │   ├── currency.py              # Currency converter
│   │   └── transportation.py        # Transport info
│   ├── providers/
│   │   ├── base.py                  # ModelProvider ABC
│   │   ├── openai_provider.py       # OpenAI implementation
│   │   └── google_provider.py       # Google Gemini implementation
│   ├── pipelines/
│   │   └── builder.py               # Pipeline builder
│   ├── display/
│   │   └── logger.py                # Rich formatting
│   ├── scenarios/
│   │   └── travel.py                # Travel scenario
│   └── main.py                      # CLI entry point
├── pyproject.toml                   # Dependencies
├── taskfile.yml                     # Task automation
└── README.md                        # This file
```

### Adding New Tools

1. Create a new file in `src/llm_tool_comparison/tools/`
2. Define mock data for reproducibility
3. Implement a Haystack component with `@component` decorator
4. Add the tool to `get_all_tools()` in `tools/__init__.py`

Example:

```python
from haystack import component
from typing import Dict

MOCK_DATA = {"key": "value"}

@component
class MyTool:
    @component.output_types(result=Dict)
    def run(self, param: str) -> Dict:
        """Tool description."""
        return {"result": MOCK_DATA.get(param, {})}
```

### Adding New Scenarios

1. Create a new file in `src/llm_tool_comparison/scenarios/`
2. Define the query and description
3. Import and use in `main.py`

### Adding New Model Providers

1. Create a new provider file in `src/llm_tool_comparison/providers/`
2. Inherit from `ModelProvider`
3. Implement `get_model_name()` and `run_conversation()`
4. Add provider logic to `main.py`

## Key Design Decisions

✅ **Mock Data** - All tools use hardcoded data for reproducible testing
✅ **Sequential Execution** - Models run one at a time for clear output
✅ **Reusable Pipeline** - Same architecture works for all providers
✅ **OpenInference** - Automatic LangFuse integration
✅ **Rich Formatting** - Professional terminal output

## Troubleshooting

### Connection Errors

Run the connection test:

```bash
python -m llm_tool_comparison.main test-connection
```

### API Key Issues

- Ensure `.env` file exists and contains valid keys
- OpenAI keys should start with `sk-`
- LangFuse keys should start with `pk-lf-` and `sk-lf-`

### Import Errors

Reinstall dependencies:

```bash
source .venv/bin/activate.fish
uv pip install -e .
```

### Tool Calling Not Working

- Check that tools are properly registered in `tools/__init__.py`
- Verify the pipeline builder connects components correctly
- Check LangFuse traces for detailed execution logs

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Contact

For questions or issues, please open an issue on GitHub.
