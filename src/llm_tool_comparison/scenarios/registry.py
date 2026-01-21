"""Scenario registry for managing available test scenarios."""

from dataclasses import dataclass
from typing import Dict

from .travel import TRAVEL_QUERY, TRAVEL_SCENARIO_DESCRIPTION
from .simple import SIMPLE_QUERY, SIMPLE_SCENARIO_DESCRIPTION
from .resort import RESORT_QUERY, RESORT_SCENARIO_DESCRIPTION, RESORT_SYSTEM_PROMPT


@dataclass
class Scenario:
    """A test scenario with query, description, and optional system prompt."""
    name: str
    query: str
    description: str
    system_prompt: str = ""


SCENARIOS: Dict[str, Scenario] = {
    "travel": Scenario(
        name="travel",
        query=TRAVEL_QUERY,
        description=TRAVEL_SCENARIO_DESCRIPTION,
    ),
    "simple": Scenario(
        name="simple",
        query=SIMPLE_QUERY,
        description=SIMPLE_SCENARIO_DESCRIPTION,
    ),
    "resort": Scenario(
        name="resort",
        query=RESORT_QUERY,
        description=RESORT_SCENARIO_DESCRIPTION,
        system_prompt=RESORT_SYSTEM_PROMPT,
    ),
}

DEFAULT_SCENARIO = "travel"


def get_scenario(name: str) -> Scenario:
    """Get a scenario by name.

    Args:
        name: Scenario name

    Returns:
        Scenario object

    Raises:
        ValueError: If scenario not found
    """
    if name not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())
        raise ValueError(f"Unknown scenario: {name}. Available: {available}")
    return SCENARIOS[name]


def list_scenarios() -> Dict[str, Scenario]:
    """List all available scenarios."""
    return SCENARIOS
