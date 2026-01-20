"""Transportation information tool with mock data."""

from typing import Dict, List
from haystack import component


# Mock transportation data
TRANSPORTATION_DATA = {
    "Tokyo": {
        "airport_access": [
            {
                "from": "Narita Airport",
                "to": "Central Tokyo",
                "method": "Narita Express (N'EX)",
                "duration": "60 minutes",
                "cost_jpy": 3070,
                "frequency": "Every 30 minutes"
            },
            {
                "from": "Haneda Airport",
                "to": "Central Tokyo",
                "method": "Tokyo Monorail",
                "duration": "20 minutes",
                "cost_jpy": 500,
                "frequency": "Every 5-10 minutes"
            }
        ],
        "local_transport": {
            "type": "Extensive rail and subway network",
            "recommendations": [
                {
                    "pass": "JR Pass (7-day)",
                    "cost_jpy": 29110,
                    "benefits": "Unlimited JR trains including Shinkansen",
                    "best_for": "Tourists planning trips outside Tokyo"
                },
                {
                    "pass": "Tokyo Metro 72-hour",
                    "cost_jpy": 1500,
                    "benefits": "Unlimited Tokyo Metro rides",
                    "best_for": "Intensive Tokyo sightseeing"
                },
                {
                    "pass": "IC Card (Suica/Pasmo)",
                    "cost_jpy": 0,
                    "benefits": "Pay-as-you-go, works everywhere",
                    "best_for": "Flexible travelers"
                }
            ]
        }
    }
}


@component
class TransportationTool:
    """Get transportation information for a city."""

    @component.output_types(transport_info=Dict)
    def run(self, city: str, info_type: str = "all") -> Dict:
        """Get transportation information.

        Args:
            city: City name (e.g., "Tokyo")
            info_type: Type of info - "airport", "local", or "all"

        Returns:
            Transportation information and recommendations
        """
        data = TRANSPORTATION_DATA.get(city, {})

        if not data:
            return {"transport_info": {
                "error": f"No transportation data available for {city}"
            }}

        result = {}

        if info_type in ["all", "airport"]:
            result["airport_access"] = data.get("airport_access", [])

        if info_type in ["all", "local"]:
            result["local_transport"] = data.get("local_transport", {})

        return {"transport_info": result}
