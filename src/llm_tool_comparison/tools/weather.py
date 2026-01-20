"""Weather forecast tool with mock data."""

from typing import Dict
from haystack import component


# Mock data for consistent, reproducible testing
WEATHER_DATA = {
    "Tokyo": {
        "April": {
            "avg_temp_c": 15,
            "avg_temp_f": 59,
            "conditions": "Mild with occasional rain",
            "rainfall_mm": 125,
            "humidity": "65%",
            "best_time": "Cherry blossom season - ideal for sightseeing"
        }
    }
}


@component
class WeatherTool:
    """Get weather forecast for a location in a specific month."""

    @component.output_types(forecast=Dict)
    def run(self, location: str, month: str) -> Dict:
        """Get weather forecast.

        Args:
            location: City name (e.g., "Tokyo")
            month: Month name (e.g., "April")

        Returns:
            Dictionary with temperature, conditions, rainfall, and travel info
        """
        data = WEATHER_DATA.get(location, {}).get(month, {
            "error": f"No weather data available for {location} in {month}"
        })
        return {"forecast": data}
