"""Tourist attractions finder tool with mock data."""

from typing import Dict, List
from haystack import component


# Mock attractions data
ATTRACTIONS_DATA = {
    "Tokyo": [
        {
            "name": "Senso-ji Temple",
            "category": "Cultural/Historical",
            "area": "Asakusa",
            "duration": "2-3 hours",
            "description": "Tokyo's oldest temple with traditional atmosphere",
            "best_time": "Morning to avoid crowds"
        },
        {
            "name": "Meiji Shrine",
            "category": "Cultural/Historical",
            "area": "Harajuku",
            "duration": "1-2 hours",
            "description": "Peaceful shrine in forested grounds",
            "best_time": "Early morning"
        },
        {
            "name": "Shibuya Crossing",
            "category": "Modern/Urban",
            "area": "Shibuya",
            "duration": "30 minutes",
            "description": "World's busiest pedestrian crossing",
            "best_time": "Evening for best atmosphere"
        },
        {
            "name": "Tokyo Skytree",
            "category": "Modern/Observation",
            "area": "Sumida",
            "duration": "2-3 hours",
            "description": "634m tall tower with panoramic views",
            "best_time": "Sunset for day and night views"
        },
        {
            "name": "Tsukiji Outer Market",
            "category": "Food/Market",
            "area": "Tsukiji",
            "duration": "2 hours",
            "description": "Fresh seafood and street food market",
            "best_time": "Morning (6-11 AM)"
        },
        {
            "name": "TeamLab Borderless",
            "category": "Art/Digital",
            "area": "Odaiba",
            "duration": "2-3 hours",
            "description": "Immersive digital art museum",
            "best_time": "Weekday afternoons"
        }
    ]
}


@component
class AttractionsTool:
    """Find tourist attractions in a city."""

    @component.output_types(attractions=List[Dict])
    def run(self, city: str, category: str = "all") -> Dict:
        """Find attractions.

        Args:
            city: City name (e.g., "Tokyo")
            category: Filter by category or "all" for everything

        Returns:
            List of attractions with details
        """
        attractions = ATTRACTIONS_DATA.get(city, [])

        if category != "all":
            attractions = [a for a in attractions if category.lower() in a["category"].lower()]

        return {"attractions": attractions}
