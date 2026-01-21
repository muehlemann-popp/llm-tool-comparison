"""Simple scenario with minimal tool calls."""

SIMPLE_QUERY = """What's the weather like in Tokio in April?"""

SIMPLE_SCENARIO_DESCRIPTION = """
Simple Weather Query Scenario

This scenario tests basic single-tool calling:
- Simple, focused query
- Single tool call expected
- Quick response validation

Expected Tool Calls:
1. get_weather_forecast(location="Tokio", month="April")

The model should provide a straightforward weather summary.
"""
