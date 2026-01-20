"""Tools module - provides mock tools for LLM comparison using Haystack Tool format."""

from haystack.tools import Tool
from typing import Dict, List


# ============================================================================
# WEATHER TOOL
# ============================================================================

WEATHER_DATA = {
    "Tokyo": {
        "April": {
            "avg_temp_celsius": 15,
            "conditions": "Mild with occasional rain",
            "rainfall_mm": 125,
            "best_time": "Cherry blossom season"
        }
    }
}


def get_weather_forecast(location: str, month: str) -> str:
    """Get weather forecast for a location in a specific month."""
    city_data = WEATHER_DATA.get(location, {})
    month_data = city_data.get(month, {})

    if not month_data:
        return f"No weather data available for {location} in {month}"

    return f"Weather in {location} for {month}: {month_data['avg_temp_celsius']}°C, {month_data['conditions']}, rainfall {month_data['rainfall_mm']}mm. {month_data['best_time']}"


# ============================================================================
# HOTEL SEARCH TOOL
# ============================================================================

HOTEL_DATA = {
    "Tokyo": {
        "Shibuya": [
            {"name": "Hotel Emit Shibuya", "price_usd": 150, "rating": 4.2, "distance_to_station": "5 min walk"},
            {"name": "Shibuya Excel Hotel Tokyu", "price_usd": 180, "rating": 4.5, "distance_to_station": "2 min walk"},
            {"name": "Cerulean Tower Tokyu Hotel", "price_usd": 195, "rating": 4.6, "distance_to_station": "Direct connection"},
        ]
    }
}


def search_hotels(city: str, area: str, max_price_usd: int = 1000) -> str:
    """Search for hotels in a specific city and area."""
    city_hotels = HOTEL_DATA.get(city, {})
    area_hotels = city_hotels.get(area, [])

    if not area_hotels:
        return f"No hotels found in {area}, {city}"

    # Filter by price
    filtered = [h for h in area_hotels if h['price_usd'] <= max_price_usd]

    if not filtered:
        return f"No hotels found under ${max_price_usd} in {area}, {city}"

    result = f"Found {len(filtered)} hotels in {area}, {city} under ${max_price_usd}/night:\n"
    for hotel in filtered:
        result += f"- {hotel['name']}: ${hotel['price_usd']}/night, {hotel['rating']}⭐, {hotel['distance_to_station']}\n"

    return result


# ============================================================================
# ATTRACTIONS TOOL
# ============================================================================

ATTRACTIONS_DATA = {
    "Tokyo": [
        {"name": "Senso-ji Temple", "category": "cultural", "area": "Asakusa", "visit_time": "1-2 hours"},
        {"name": "Tokyo Skytree", "category": "landmark", "area": "Sumida", "visit_time": "2-3 hours"},
        {"name": "Meiji Shrine", "category": "cultural", "area": "Harajuku", "visit_time": "1-2 hours"},
        {"name": "Tsukiji Outer Market", "category": "food", "area": "Tsukiji", "visit_time": "2-3 hours"},
        {"name": "teamLab Borderless", "category": "entertainment", "area": "Odaiba", "visit_time": "2-4 hours"},
    ]
}


def find_attractions(city: str, category: str = "all") -> str:
    """Find tourist attractions in a city, optionally filtered by category."""
    attractions = ATTRACTIONS_DATA.get(city, [])

    if not attractions:
        return f"No attractions found for {city}"

    if category != "all":
        attractions = [a for a in attractions if a['category'] == category]

    if not attractions:
        return f"No {category} attractions found in {city}"

    result = f"Found {len(attractions)} attractions in {city}:\n"
    for attr in attractions:
        result += f"- {attr['name']} ({attr['category']}): {attr['area']}, visit time: {attr['visit_time']}\n"

    return result


# ============================================================================
# CURRENCY CONVERTER TOOL
# ============================================================================

EXCHANGE_RATES = {
    "USD_TO_JPY": 149.50,
    "JPY_TO_USD": 0.0067,
}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency between USD and JPY."""
    key = f"{from_currency}_TO_{to_currency}"
    rate = EXCHANGE_RATES.get(key)

    if not rate:
        return f"Exchange rate not available for {from_currency} to {to_currency}"

    converted = amount * rate
    return f"{amount} {from_currency} = {converted:.2f} {to_currency} (rate: {rate})"


# ============================================================================
# TRANSPORTATION TOOL
# ============================================================================

TRANSPORTATION_DATA = {
    "Tokyo": {
        "airport_access": "Narita Express: 60min, ¥3,070 | Haneda Monorail: 20min, ¥500",
        "local_transport": "JR Pass (7-day): ¥29,110 | Tokyo Metro 72h: ¥1,500 | IC Card (Suica): Pay-per-ride"
    }
}


def get_transportation_info(city: str) -> str:
    """Get transportation information for a city."""
    info = TRANSPORTATION_DATA.get(city)

    if not info:
        return f"No transportation data for {city}"

    return f"Transportation in {city}:\nAirport access: {info['airport_access']}\nLocal transport: {info['local_transport']}"


# ============================================================================
# TOOL REGISTRY
# ============================================================================

def get_all_tools() -> List[Tool]:
    """Get instances of all available tools in Haystack Tool format.

    Returns:
        List of Tool instances ready for use in pipelines
    """
    return [
        Tool(
            name="get_weather_forecast",
            description="Get weather forecast for a location in a specific month",
            parameters={
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name (e.g., Tokyo)"},
                    "month": {"type": "string", "description": "Month name (e.g., April)"},
                },
                "required": ["location", "month"],
            },
            function=get_weather_forecast,
        ),
        Tool(
            name="search_hotels",
            description="Search for hotels in a city/area with price filtering",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "area": {"type": "string", "description": "Area or neighborhood name"},
                    "max_price_usd": {"type": "integer", "description": "Maximum price per night in USD", "default": 1000},
                },
                "required": ["city", "area"],
            },
            function=search_hotels,
        ),
        Tool(
            name="find_attractions",
            description="Find tourist attractions in a city",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "category": {"type": "string", "description": "Category: cultural, landmark, food, entertainment, or all", "default": "all"},
                },
                "required": ["city"],
            },
            function=find_attractions,
        ),
        Tool(
            name="convert_currency",
            description="Convert between USD and JPY currencies",
            parameters={
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount to convert"},
                    "from_currency": {"type": "string", "description": "Source currency (USD or JPY)"},
                    "to_currency": {"type": "string", "description": "Target currency (USD or JPY)"},
                },
                "required": ["amount", "from_currency", "to_currency"],
            },
            function=convert_currency,
        ),
        Tool(
            name="get_transportation_info",
            description="Get transportation information for a city including airport access and local transport options",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                },
                "required": ["city"],
            },
            function=get_transportation_info,
        ),
    ]


__all__ = [
    "get_weather_forecast",
    "search_hotels",
    "find_attractions",
    "convert_currency",
    "get_transportation_info",
    "get_all_tools",
]
