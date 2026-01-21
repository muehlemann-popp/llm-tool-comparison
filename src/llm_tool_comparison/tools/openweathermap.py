"""OpenWeatherMap mock tools for weather forecasts."""

from typing import Dict, List
from haystack import component


# Mock weather data for Swiss locations
WEATHER_FORECASTS = {
    "Andeer, Switzerland": [
        {"date": "2026-02-02", "temp_high": 2, "temp_low": -5, "conditions": "Partly cloudy", "precipitation": "10%"},
        {"date": "2026-02-03", "temp_high": 1, "temp_low": -6, "conditions": "Light snow", "precipitation": "60%"},
        {"date": "2026-02-04", "temp_high": 0, "temp_low": -7, "conditions": "Snow", "precipitation": "80%"},
        {"date": "2026-02-05", "temp_high": -1, "temp_low": -8, "conditions": "Cloudy", "precipitation": "20%"},
        {"date": "2026-02-06", "temp_high": 1, "temp_low": -5, "conditions": "Sunny", "precipitation": "5%"},
        {"date": "2026-02-07", "temp_high": 3, "temp_low": -4, "conditions": "Partly cloudy", "precipitation": "15%"},
        {"date": "2026-02-08", "temp_high": 2, "temp_low": -6, "conditions": "Light snow", "precipitation": "45%"},
    ],
    "Splügen, Switzerland": [
        {"date": "2026-02-02", "temp_high": -1, "temp_low": -8, "conditions": "Snow", "precipitation": "70%"},
        {"date": "2026-02-03", "temp_high": -2, "temp_low": -9, "conditions": "Heavy snow", "precipitation": "90%"},
        {"date": "2026-02-04", "temp_high": -3, "temp_low": -10, "conditions": "Snow", "precipitation": "85%"},
        {"date": "2026-02-05", "temp_high": -2, "temp_low": -9, "conditions": "Cloudy", "precipitation": "30%"},
        {"date": "2026-02-06", "temp_high": 0, "temp_low": -7, "conditions": "Partly cloudy", "precipitation": "20%"},
        {"date": "2026-02-07", "temp_high": 1, "temp_low": -6, "conditions": "Sunny", "precipitation": "5%"},
        {"date": "2026-02-08", "temp_high": 0, "temp_low": -8, "conditions": "Light snow", "precipitation": "55%"},
    ],
}


# Default weather data for any unknown location
DEFAULT_WEATHER = [
    {"date": "2026-02-02", "temp_high": 3, "temp_low": -4, "conditions": "Partly cloudy", "precipitation": "15%"},
    {"date": "2026-02-03", "temp_high": 2, "temp_low": -5, "conditions": "Light snow", "precipitation": "50%"},
    {"date": "2026-02-04", "temp_high": 1, "temp_low": -6, "conditions": "Cloudy", "precipitation": "30%"},
    {"date": "2026-02-05", "temp_high": 0, "temp_low": -7, "conditions": "Snow", "precipitation": "70%"},
    {"date": "2026-02-06", "temp_high": 2, "temp_low": -5, "conditions": "Sunny", "precipitation": "10%"},
    {"date": "2026-02-07", "temp_high": 4, "temp_low": -3, "conditions": "Partly cloudy", "precipitation": "20%"},
    {"date": "2026-02-08", "temp_high": 3, "temp_low": -4, "conditions": "Light snow", "precipitation": "40%"},
]


@component
class OWMDailyForecastTool:
    """Get daily weather forecast for a city using OpenWeatherMap-style API."""

    @component.output_types(forecast=List[Dict])
    def run(self, city: str, days: int = 7) -> Dict:
        """Get daily weather forecast.

        Args:
            city: City name with country (e.g., "Andeer, Switzerland")
            days: Number of days to forecast (1-7)

        Returns:
            List of daily forecasts with temperature and conditions
        """
        days = min(max(days, 1), 7)  # Clamp to 1-7 days

        # Try exact match first, then partial match, then default
        forecasts = WEATHER_FORECASTS.get(city)

        if not forecasts:
            # Try partial match (case-insensitive)
            city_lower = city.lower()
            for known_city, data in WEATHER_FORECASTS.items():
                if city_lower in known_city.lower() or known_city.lower() in city_lower:
                    forecasts = data
                    break

        # Fall back to default weather data
        if not forecasts:
            forecasts = DEFAULT_WEATHER

        return {"forecast": forecasts[:days]}


def owm_daily_forecast(city: str, days: int = 7) -> str:
    """Get daily weather forecast for a city.

    Args:
        city: City name with country (e.g., "Andeer, Switzerland")
        days: Number of days to forecast (1-7)

    Returns:
        Formatted weather forecast string
    """
    tool = OWMDailyForecastTool()
    result = tool.run(city=city, days=days)
    forecasts = result["forecast"]

    output = f"Weather forecast for {city} ({days} days):\n"
    for day in forecasts:
        output += f"  {day['date']}: {day['temp_high']}°C/{day['temp_low']}°C, {day['conditions']}, precip: {day['precipitation']}\n"

    return output
