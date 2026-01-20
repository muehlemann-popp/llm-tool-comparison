"""Hotel search tool with mock data."""

from typing import Dict, List
from haystack import component


# Mock hotel data
HOTEL_DATA = {
    "Tokyo": {
        "Shibuya": [
            {
                "name": "Shibuya Excel Hotel Tokyu",
                "price_per_night": 180,
                "rating": 4.5,
                "distance_to_center": "0.2 km",
                "amenities": ["WiFi", "Restaurant", "Gym", "City View"]
            },
            {
                "name": "Hotel Metropolitan Shibuya",
                "price_per_night": 195,
                "rating": 4.3,
                "distance_to_center": "0.3 km",
                "amenities": ["WiFi", "Restaurant", "Bar", "Meeting Rooms"]
            },
            {
                "name": "Shibuya Granbell Hotel",
                "price_per_night": 165,
                "rating": 4.4,
                "distance_to_center": "0.5 km",
                "amenities": ["WiFi", "Rooftop Bar", "Modern Design"]
            }
        ]
    }
}


@component
class HotelSearchTool:
    """Search for hotels in a specific area."""

    @component.output_types(hotels=List[Dict])
    def run(self, city: str, area: str, max_price: int = 300) -> Dict:
        """Search for hotels.

        Args:
            city: City name (e.g., "Tokyo")
            area: Area/neighborhood (e.g., "Shibuya")
            max_price: Maximum price per night in USD

        Returns:
            List of hotels matching criteria
        """
        all_hotels = HOTEL_DATA.get(city, {}).get(area, [])
        filtered_hotels = [h for h in all_hotels if h["price_per_night"] <= max_price]

        return {"hotels": filtered_hotels}
