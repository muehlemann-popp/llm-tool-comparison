"""Scenarios module for testing different use cases."""

from .travel import TRAVEL_QUERY, TRAVEL_SCENARIO_DESCRIPTION
from .simple import SIMPLE_QUERY, SIMPLE_SCENARIO_DESCRIPTION
from .resort import RESORT_QUERY, RESORT_SCENARIO_DESCRIPTION, RESORT_SYSTEM_PROMPT
from .registry import Scenario, get_scenario, list_scenarios, DEFAULT_SCENARIO

__all__ = [
    "TRAVEL_QUERY",
    "TRAVEL_SCENARIO_DESCRIPTION",
    "SIMPLE_QUERY",
    "SIMPLE_SCENARIO_DESCRIPTION",
    "RESORT_QUERY",
    "RESORT_SCENARIO_DESCRIPTION",
    "RESORT_SYSTEM_PROMPT",
    "Scenario",
    "get_scenario",
    "list_scenarios",
    "DEFAULT_SCENARIO",
]
