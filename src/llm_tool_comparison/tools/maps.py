"""Google Maps-style mock tools for places search and details."""

from typing import Dict, List, Optional
from haystack import component


# Mock places data organized by type and location
PLACES_DATABASE = {
    "gas_station": [
        {
            "place_id": "ChIJEclCVhTthEcRzapd5iduJCs",
            "name": "Avia Tankstelle Andeer",
            "address": "Hauptstrasse 42, 7440 Andeer, Switzerland",
            "location": {"lat": 46.6089, "lng": 9.4312},
            "rating": 4.2,
            "price_level": 2,
            "types": ["gas_station", "car_wash"],
            "opening_hours": "06:00-22:00",
            "has_ev_charging": True,
            "ev_charger_types": ["Type 2 (22kW)"],
        },
        {
            "place_id": "ChIJ8Yz9jhzthEcRQwzXxL5gZxE",
            "name": "Shell Thusis",
            "address": "Compognastrasse 15, 7430 Thusis, Switzerland",
            "location": {"lat": 46.6973, "lng": 9.4396},
            "rating": 4.0,
            "price_level": 2,
            "types": ["gas_station", "convenience_store"],
            "opening_hours": "24 hours",
            "has_ev_charging": True,
            "ev_charger_types": ["CCS (50kW)", "Type 2 (22kW)"],
        },
    ],
    "restaurant": [
        {
            "place_id": "ChIJRestaurant001",
            "name": "Restaurant Fravi",
            "address": "Via Sorts 1, 7440 Andeer, Switzerland",
            "location": {"lat": 46.6098, "lng": 9.4289},
            "rating": 4.5,
            "price_level": 3,
            "types": ["restaurant", "swiss_cuisine"],
            "opening_hours": "11:30-14:00, 18:00-21:30",
            "cuisine": "Traditional Swiss",
            "specialties": ["Capuns", "Pizzoccheri", "Local game"],
        },
        {
            "place_id": "ChIJRestaurant002",
            "name": "Gasthaus zum Steinbock",
            "address": "Dorfplatz 8, 7435 Splügen, Switzerland",
            "location": {"lat": 46.5506, "lng": 9.3177},
            "rating": 4.3,
            "price_level": 2,
            "types": ["restaurant", "bar"],
            "opening_hours": "10:00-23:00",
            "cuisine": "Swiss-Italian",
        },
        {
            "place_id": "ChIJRestaurant003",
            "name": "Ristorante Piz Tambo",
            "address": "Via Cantonale, 7435 Splügen, Switzerland",
            "location": {"lat": 46.5489, "lng": 9.3201},
            "rating": 4.1,
            "price_level": 2,
            "types": ["restaurant", "pizzeria"],
            "opening_hours": "11:00-22:00",
            "cuisine": "Italian",
        },
    ],
    "spa": [
        {
            "place_id": "ChIJMineralbad001",
            "name": "Mineralbad Andeer",
            "address": "Via Bogn 52, 7440 Andeer, Switzerland",
            "location": {"lat": 46.6067, "lng": 9.4267},
            "rating": 4.6,
            "price_level": 2,
            "types": ["spa", "thermal_bath", "wellness"],
            "opening_hours": "10:00-21:00",
            "features": ["Mineral thermal water", "Indoor & outdoor pools", "Sauna", "Steam bath"],
            "entry_fee_chf": 25,
        },
    ],
    "lodging": [
        {
            "place_id": "ChIJHotel001",
            "name": "Hotel & Restaurant Fravi",
            "address": "Via Sorts 1, 7440 Andeer, Switzerland",
            "location": {"lat": 46.6098, "lng": 9.4289},
            "rating": 4.4,
            "price_level": 3,
            "types": ["lodging", "hotel", "restaurant"],
            "rooms_from_chf": 140,
        },
        {
            "place_id": "ChIJHotel002",
            "name": "Gasthaus Rofflaschlucht",
            "address": "Rofflaschlucht, 7433 Andeer, Switzerland",
            "location": {"lat": 46.5833, "lng": 9.4000},
            "rating": 4.2,
            "price_level": 2,
            "types": ["lodging", "guesthouse"],
            "rooms_from_chf": 95,
        },
    ],
    "point_of_interest": [
        {
            "place_id": "ChIJSki001",
            "name": "Skigebiet Splügen-Tambo",
            "address": "7435 Splügen, Switzerland",
            "location": {"lat": 46.5506, "lng": 9.3177},
            "rating": 4.4,
            "types": ["ski_area", "point_of_interest"],
            "features": ["30km slopes", "6 lifts", "Snow park", "Night skiing"],
            "ski_pass_day_chf": 52,
        },
        {
            "place_id": "ChIJSki002",
            "name": "Sport Mengelt - Ski Rental",
            "address": "Via Cantonale 12, 7435 Splügen, Switzerland",
            "location": {"lat": 46.5498, "lng": 9.3189},
            "rating": 4.7,
            "types": ["ski_rental", "point_of_interest", "store"],
            "opening_hours": "08:00-18:00",
            "services": ["Ski rental", "Snowboard rental", "Equipment service"],
        },
        {
            "place_id": "ChIJRental001",
            "name": "Intersport Andeer",
            "address": "Hauptstrasse 28, 7440 Andeer, Switzerland",
            "location": {"lat": 46.6092, "lng": 9.4301},
            "rating": 4.3,
            "types": ["ski_rental", "store", "point_of_interest"],
            "opening_hours": "08:30-12:00, 14:00-18:00",
            "services": ["Ski rental", "Winter clothing", "Equipment repair"],
        },
    ],
    "supermarket": [
        {
            "place_id": "ChIJVolg001",
            "name": "Volg Andeer",
            "address": "Hauptstrasse 15, 7440 Andeer, Switzerland",
            "location": {"lat": 46.6095, "lng": 9.4295},
            "rating": 4.1,
            "price_level": 2,
            "types": ["supermarket", "grocery_store"],
            "opening_hours": "07:30-12:00, 14:00-18:30 (Sat: 07:30-16:00)",
        },
        {
            "place_id": "ChIJCoop001",
            "name": "Coop Thusis",
            "address": "Neudorfstrasse 60, 7430 Thusis, Switzerland",
            "location": {"lat": 46.6967, "lng": 9.4412},
            "rating": 4.2,
            "price_level": 2,
            "types": ["supermarket", "grocery_store"],
            "opening_hours": "08:00-20:00 (Sat: 08:00-18:00)",
        },
    ],
    "parking": [
        {
            "place_id": "ChIJParking001",
            "name": "Parkhaus Andeer",
            "address": "Dorfstrasse, 7440 Andeer, Switzerland",
            "location": {"lat": 46.6088, "lng": 9.4278},
            "rating": 4.0,
            "types": ["parking", "ev_charging"],
            "has_ev_charging": True,
            "ev_charger_types": ["Type 2 (11kW)"],
            "fee_per_hour_chf": 2,
        },
    ],
}

# Detailed place information (extended data for specific places)
PLACE_DETAILS = {
    "ChIJEclCVhTthEcRzapd5iduJCs": {
        "place_id": "ChIJEclCVhTthEcRzapd5iduJCs",
        "name": "Avia Tankstelle Andeer",
        "formatted_address": "Hauptstrasse 42, 7440 Andeer, Switzerland",
        "formatted_phone_number": "+41 81 661 12 34",
        "website": "https://www.avia.ch",
        "location": {"lat": 46.6089, "lng": 9.4312},
        "rating": 4.2,
        "user_ratings_total": 87,
        "price_level": 2,
        "types": ["gas_station", "car_wash", "ev_charging_station"],
        "opening_hours": {
            "weekday_text": [
                "Monday: 06:00-22:00",
                "Tuesday: 06:00-22:00",
                "Wednesday: 06:00-22:00",
                "Thursday: 06:00-22:00",
                "Friday: 06:00-22:00",
                "Saturday: 07:00-21:00",
                "Sunday: 08:00-20:00",
            ]
        },
        "reviews": [
            {"author": "Hans M.", "rating": 5, "text": "Clean station, friendly staff. EV charger works great!"},
            {"author": "Maria K.", "rating": 4, "text": "Good location, fair prices for the region."},
        ],
        "ev_charging": {
            "available": True,
            "chargers": [
                {"type": "Type 2", "power_kw": 22, "connector_count": 2},
            ],
            "pricing": "CHF 0.45/kWh",
            "payment": ["Credit card", "RFID", "App"],
        },
    },
    "ChIJMineralbad001": {
        "place_id": "ChIJMineralbad001",
        "name": "Mineralbad Andeer",
        "formatted_address": "Via Bogn 52, 7440 Andeer, Switzerland",
        "formatted_phone_number": "+41 81 661 14 44",
        "website": "https://www.mineralbad-andeer.ch",
        "location": {"lat": 46.6067, "lng": 9.4267},
        "rating": 4.6,
        "user_ratings_total": 523,
        "price_level": 2,
        "types": ["spa", "thermal_bath", "wellness", "point_of_interest"],
        "opening_hours": {
            "weekday_text": [
                "Monday: 10:00-21:00",
                "Tuesday: 10:00-21:00",
                "Wednesday: 10:00-21:00",
                "Thursday: 10:00-21:00",
                "Friday: 10:00-21:00",
                "Saturday: 10:00-21:00",
                "Sunday: 10:00-21:00",
            ]
        },
        "reviews": [
            {"author": "Sophie L.", "rating": 5, "text": "Amazing mineral water! Very relaxing atmosphere."},
            {"author": "Thomas B.", "rating": 4, "text": "Beautiful facility, can get crowded on weekends."},
        ],
        "description": "Historic thermal bath with natural mineral springs. Water temperature 34°C. Features indoor and outdoor pools, sauna, steam bath, and relaxation areas.",
        "prices": {
            "adult_2h": 25,
            "adult_day": 35,
            "child_2h": 15,
            "sauna_supplement": 10,
        },
    },
}


def _filter_by_location(places: List[Dict], location: str, radius: int) -> List[Dict]:
    """Filter places by approximate location matching.

    Always returns data - if no specific match, returns all places for mock purposes.
    """
    if not places:
        return places

    # Simple text-based location matching for mock data
    location_lower = location.lower()

    # Check for coordinates
    if "," in location and any(c.isdigit() for c in location):
        # Assume it's coordinates - return all places within region
        return places

    # Text-based matching
    filtered = []
    for place in places:
        addr_lower = place.get("address", "").lower()
        if any(loc_part in addr_lower for loc_part in location_lower.split(",")):
            filtered.append(place)

    # If no match, return all (for mock purposes - always return data)
    return filtered if filtered else places


def _filter_by_keyword(places: List[Dict], keyword: str) -> List[Dict]:
    """Filter places by keyword in name, types, or features.

    Always returns data - if no keyword match, returns all places for mock purposes.
    """
    if not keyword or not places:
        return places

    keyword_lower = keyword.lower()
    filtered = []

    for place in places:
        name = place.get("name", "").lower()
        types = " ".join(place.get("types", [])).lower()
        features = " ".join(place.get("features", [])).lower() if "features" in place else ""
        services = " ".join(place.get("services", [])).lower() if "services" in place else ""

        searchable = f"{name} {types} {features} {services}"

        if keyword_lower in searchable:
            filtered.append(place)

    # If no match, return all (for mock purposes - always return data)
    return filtered if filtered else places


@component
class MapsSearchNearbyPlacesTool:
    """Search for places near a location using Google Maps-style API."""

    @component.output_types(places=List[Dict])
    def run(
        self,
        location: str,
        place_type: str,
        radius: int = 5000,
        keyword: str = "",
        lang_code: str = "en",
        min_price: int = 0,
        max_price: int = 4,
    ) -> Dict:
        """Search for nearby places.

        Args:
            location: Location as address or "lat,lng" coordinates
            place_type: Type of place (restaurant, gas_station, spa, etc.)
            radius: Search radius in meters
            keyword: Optional keyword to filter results
            lang_code: Language code for results
            min_price: Minimum price level (0-4)
            max_price: Maximum price level (0-4)

        Returns:
            List of matching places
        """
        places = PLACES_DATABASE.get(place_type, [])

        # If place_type not found, try to find similar or return point_of_interest
        if not places:
            places = PLACES_DATABASE.get("point_of_interest", [])

        # Apply filters
        places = _filter_by_location(places, location, radius)
        places = _filter_by_keyword(places, keyword)

        # Filter by price level
        places = [
            p for p in places
            if min_price <= p.get("price_level", 2) <= max_price
        ]

        return {"places": places}


@component
class MapsGetPlacesDetailsTool:
    """Get detailed information about specific places."""

    @component.output_types(place_details=List[Dict])
    def run(self, place_ids: List[str], lang_code: str = "en") -> Dict:
        """Get detailed place information.

        Args:
            place_ids: List of place IDs to get details for
            lang_code: Language code for results

        Returns:
            List of detailed place information
        """
        details = []
        for place_id in place_ids:
            if place_id in PLACE_DETAILS:
                details.append(PLACE_DETAILS[place_id])
            else:
                # Return basic info if detailed data not available
                for place_type, places in PLACES_DATABASE.items():
                    for place in places:
                        if place.get("place_id") == place_id:
                            details.append(place)
                            break

        return {"place_details": details}


# Function-based tools for direct use

def maps_search_nearby_places(
    location: str,
    place_type: str,
    radius: int = 5000,
    keyword: str = "",
    lang_code: str = "en",
    min_price: int = 0,
    max_price: int = 4,
) -> str:
    """Search for nearby places.

    Args:
        location: Location as address or coordinates
        place_type: Type of place to search for
        radius: Search radius in meters
        keyword: Optional search keyword
        lang_code: Language code
        min_price: Minimum price level (0-4)
        max_price: Maximum price level (0-4)

    Returns:
        Formatted string of matching places
    """
    tool = MapsSearchNearbyPlacesTool()
    result = tool.run(
        location=location,
        place_type=place_type,
        radius=radius,
        keyword=keyword,
        lang_code=lang_code,
        min_price=min_price,
        max_price=max_price,
    )
    places = result["places"]

    if not places:
        return f"No {place_type} found near {location} matching '{keyword}'"

    output = f"Found {len(places)} {place_type}(s) near {location}:\n"
    for place in places:
        output += f"\n  {place['name']}\n"
        output += f"    Address: {place['address']}\n"
        output += f"    Rating: {place.get('rating', 'N/A')}/5\n"
        if "opening_hours" in place:
            output += f"    Hours: {place['opening_hours']}\n"
        if place.get("has_ev_charging"):
            output += f"    EV Charging: Yes ({', '.join(place.get('ev_charger_types', []))})\n"
        output += f"    Place ID: {place['place_id']}\n"

    return output


def maps_get_places_details(place_ids: List[str], lang_code: str = "en") -> str:
    """Get detailed information about specific places.

    Args:
        place_ids: List of place IDs
        lang_code: Language code

    Returns:
        Formatted string with detailed place information
    """
    tool = MapsGetPlacesDetailsTool()
    result = tool.run(place_ids=place_ids, lang_code=lang_code)
    details = result["place_details"]

    if not details:
        return f"No details found for place IDs: {place_ids}"

    output = "Place Details:\n"
    for place in details:
        output += f"\n{'='*50}\n"
        output += f"{place['name']}\n"
        output += f"Address: {place.get('formatted_address', place.get('address', 'N/A'))}\n"

        if "formatted_phone_number" in place:
            output += f"Phone: {place['formatted_phone_number']}\n"
        if "website" in place:
            output += f"Website: {place['website']}\n"

        output += f"Rating: {place.get('rating', 'N/A')}/5"
        if "user_ratings_total" in place:
            output += f" ({place['user_ratings_total']} reviews)"
        output += "\n"

        if "opening_hours" in place and isinstance(place["opening_hours"], dict):
            output += "Hours:\n"
            for day in place["opening_hours"].get("weekday_text", []):
                output += f"  {day}\n"

        if "description" in place:
            output += f"\nDescription: {place['description']}\n"

        if "ev_charging" in place:
            ev = place["ev_charging"]
            output += f"\nEV Charging:\n"
            for charger in ev.get("chargers", []):
                output += f"  - {charger['type']}: {charger['power_kw']}kW ({charger['connector_count']}x)\n"
            output += f"  Pricing: {ev.get('pricing', 'N/A')}\n"

        if "prices" in place:
            output += "\nPrices:\n"
            for price_type, amount in place["prices"].items():
                output += f"  {price_type}: CHF {amount}\n"

    return output
