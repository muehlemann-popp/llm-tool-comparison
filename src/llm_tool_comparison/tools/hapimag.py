"""Hapimag resort mock tools for vacation planning scenarios."""

from typing import Dict, List
from haystack import component

# Default resort ID for fallback
DEFAULT_RESORT_ID = 1


# Mock resort data
RESORTS = {
    1: {
        "name": "Hapimag Resort Andeer",
        "location": "Andeer, Switzerland",
        "address": "Veia da Vischnanca 8, 7442 Clugin, Switzerland",
        "coordinates": {"lat": 46.6133, "lng": 9.4186},
        "description": "A charming alpine resort in the heart of Graubünden, perfect for skiing and thermal baths.",
        "rating": 4.5,
        "amenities": ["WiFi", "Parking", "Restaurant", "Spa access", "Ski storage"],
    }
}

APARTMENTS = {
    1: [
        {
            "id": "apt_101",
            "name": "Alpine Studio",
            "type": "Studio",
            "max_guests": 2,
            "bedrooms": 0,
            "size_sqm": 35,
            "amenities": ["Kitchen", "Balcony", "Mountain view"],
            "price_per_night_points": 15,
        },
        {
            "id": "apt_201",
            "name": "Mountain View Suite",
            "type": "1-Bedroom",
            "max_guests": 4,
            "bedrooms": 1,
            "size_sqm": 55,
            "amenities": ["Full kitchen", "Living room", "Balcony", "Mountain view", "Fireplace"],
            "price_per_night_points": 25,
        },
        {
            "id": "apt_301",
            "name": "Family Chalet",
            "type": "2-Bedroom",
            "max_guests": 6,
            "bedrooms": 2,
            "size_sqm": 85,
            "amenities": ["Full kitchen", "Living room", "2 Balconies", "Mountain view", "Fireplace", "Sauna"],
            "price_per_night_points": 40,
        },
    ]
}

CHARGING_STATIONS = {
    1: {
        "available": True,
        "location": "Underground parking level -1",
        "chargers": [
            {"type": "Type 2", "power_kw": 22, "count": 2, "status": "available"},
            {"type": "CCS", "power_kw": 50, "count": 1, "status": "available"},
        ],
        "pricing": "Free for guests",
        "reservation_required": False,
    }
}

GASTRONOMY = {
    1: {
        "restaurants": [
            {
                "name": "Alpenstube",
                "cuisine": "Traditional Swiss",
                "hours": "18:00-21:30",
                "dress_code": "Smart casual",
                "reservation_required": True,
                "specialties": ["Fondue", "Raclette", "Bündnerfleisch"],
            }
        ],
        "bars": [
            {
                "name": "Bergbar",
                "hours": "16:00-23:00",
                "offerings": ["Local wines", "Craft beers", "Cocktails", "Light snacks"],
            }
        ],
        "breakfast": {
            "included": True,
            "hours": "07:00-10:00",
            "style": "Buffet",
        },
    }
}

ACTIVITIES = {
    1: {
        "overview": [
            {
                "id": "activity_id:123",
                "name": "Guided Snowshoe Hike",
                "category": "Winter Sports",
                "dates_available": ["2026-02-05", "2026-02-12", "2026-02-19"],
                "duration": "3 hours",
                "difficulty": "Moderate",
                "price_chf": 45,
            },
            {
                "id": "activity_id:124",
                "name": "Thermal Bath Visit (Andeer)",
                "category": "Wellness",
                "dates_available": ["Daily"],
                "duration": "Half day",
                "difficulty": "Easy",
                "price_chf": 25,
            },
            {
                "id": "activity_id:125",
                "name": "Ski Day Trip to Splügen",
                "category": "Winter Sports",
                "dates_available": ["2026-02-03", "2026-02-10", "2026-02-17"],
                "duration": "Full day",
                "difficulty": "Various",
                "price_chf": 60,
            },
            {
                "id": "activity_id:126",
                "name": "Wine Tasting Evening",
                "category": "Culinary",
                "dates_available": ["2026-02-07", "2026-02-14"],
                "duration": "2 hours",
                "difficulty": "Easy",
                "price_chf": 35,
            },
        ]
    }
}

ACTIVITY_DETAILS = {
    "activity_id:123": {
        "name": "Guided Snowshoe Hike",
        "full_description": "Experience the winter wonderland of the Swiss Alps on this guided snowshoe adventure. Explore pristine snow-covered trails with panoramic mountain views.",
        "included": ["Snowshoe rental", "Guide", "Hot chocolate break"],
        "what_to_bring": ["Warm clothing", "Waterproof boots", "Sunglasses", "Camera"],
        "meeting_point": "Resort lobby",
        "group_size": "4-12 participants",
        "cancellation_policy": "Free cancellation up to 24h before",
    },
    "activity_id:124": {
        "name": "Thermal Bath Visit (Andeer)",
        "full_description": "Relax in the famous mineral-rich thermal waters of Andeer. The natural springs have been used for wellness since Roman times.",
        "included": ["Entrance ticket", "Locker", "Towel rental available"],
        "what_to_bring": ["Swimsuit", "Flip-flops", "Bathrobe (optional)"],
        "meeting_point": "Self-guided (5 min walk from resort)",
        "opening_hours": "10:00-21:00",
        "cancellation_policy": "Non-refundable",
    },
}

SERVICES = {
    1: {
        "reception": {"hours": "07:00-22:00", "languages": ["German", "English", "Italian", "French"]},
        "housekeeping": {"frequency": "Daily (on request)", "towel_change": "Every 3 days"},
        "laundry": {"available": True, "self_service": True, "price": "CHF 5 per load"},
        "ski_storage": {"available": True, "heated": True, "boot_dryer": True},
        "grocery_delivery": {"available": True, "partner": "Volg Andeer", "order_deadline": "18:00 day before"},
        "shuttle_service": {
            "available": True,
            "destinations": ["Splügen ski area", "Andeer thermal bath", "Thusis train station"],
            "schedule": "On request",
        },
    }
}

PET_CHARGES = {
    1: {
        "pets_allowed": True,
        "charge_per_night_chf": 15,
        "max_pets": 2,
        "restrictions": ["Dogs and cats only", "Must be declared at booking", "Not allowed in restaurant"],
        "amenities": ["Dog walking area", "Pet bed available on request"],
    }
}


# Component-based tools for Haystack pipelines

@component
class HapimagGetResortDetailsTool:
    """Get detailed information about a Hapimag resort."""

    @component.output_types(resort=Dict)
    def run(self, resort_id: int, locale: str = "en_GB") -> Dict:
        """Get resort details."""
        # Fallback to default resort if not found
        resort = RESORTS.get(resort_id) or RESORTS.get(DEFAULT_RESORT_ID)
        return {"resort": resort}


@component
class HapimagGetResortApartmentsTool:
    """Get available apartments at a Hapimag resort."""

    @component.output_types(apartments=List[Dict])
    def run(self, resort_id: int) -> Dict:
        """Get apartments for a resort."""
        apartments = APARTMENTS.get(resort_id) or APARTMENTS.get(DEFAULT_RESORT_ID, [])
        return {"apartments": apartments}


@component
class HapimagGetChargingStationTool:
    """Get EV charging station information for a resort."""

    @component.output_types(charging_station=Dict)
    def run(self, resort_id: int) -> Dict:
        """Get charging station info."""
        station = CHARGING_STATIONS.get(resort_id) or CHARGING_STATIONS.get(DEFAULT_RESORT_ID)
        if not station:
            return {"charging_station": {"available": False, "message": "No charging stations at this resort"}}
        return {"charging_station": station}


@component
class HapimagGetGastronomyDetailsTool:
    """Get restaurant and dining information for a resort."""

    @component.output_types(gastronomy=Dict)
    def run(self, resort_id: int, locale: str = "en_GB") -> Dict:
        """Get gastronomy details."""
        gastronomy = GASTRONOMY.get(resort_id) or GASTRONOMY.get(DEFAULT_RESORT_ID)
        if not gastronomy:
            return {"gastronomy": {"error": f"No gastronomy info for resort {resort_id}"}}
        return {"gastronomy": gastronomy}


@component
class HapimagGetActivitiesOverviewTool:
    """Get overview of activities available at a resort."""

    @component.output_types(activities=List[Dict])
    def run(self, resort_id: int, date_from: str, date_to: str, locale: str = "en_GB") -> Dict:
        """Get activities overview."""
        activities_data = ACTIVITIES.get(resort_id) or ACTIVITIES.get(DEFAULT_RESORT_ID, {})
        activities = activities_data.get("overview", [])
        return {"activities": activities}


@component
class HapimagGetActivitiesDetailsTool:
    """Get detailed information about specific activities."""

    @component.output_types(activity_details=List[Dict])
    def run(self, keys: List[str], date_from: str, date_to: str, locale: str = "en_GB") -> Dict:
        """Get detailed activity information."""
        details = []
        for key in keys:
            detail = ACTIVITY_DETAILS.get(key)
            if detail:
                details.append(detail)
        return {"activity_details": details}


@component
class HapimagGetResortServicesTool:
    """Get services available at a resort."""

    @component.output_types(services=Dict)
    def run(self, resort_id: int) -> Dict:
        """Get resort services."""
        services = SERVICES.get(resort_id) or SERVICES.get(DEFAULT_RESORT_ID)
        if not services:
            return {"services": {"error": f"No services info for resort {resort_id}"}}
        return {"services": services}


@component
class HapimagGetPetChargeTool:
    """Get pet policy and charges for a resort."""

    @component.output_types(pet_policy=Dict)
    def run(self, resort_id: int) -> Dict:
        """Get pet charges and policy."""
        pet_info = PET_CHARGES.get(resort_id) or PET_CHARGES.get(DEFAULT_RESORT_ID)
        if not pet_info:
            return {"pet_policy": {"pets_allowed": False, "message": "Pets not allowed at this resort"}}
        return {"pet_policy": pet_info}


# Function-based tools for direct use

def hapimag_get_resort_details(resort_id: int, locale: str = "en_GB") -> str:
    """Get detailed information about a Hapimag resort."""
    tool = HapimagGetResortDetailsTool()
    result = tool.run(resort_id=resort_id, locale=locale)
    resort = result["resort"]

    return (
        f"Resort: {resort['name']}\n"
        f"Location: {resort['location']}\n"
        f"Address: {resort['address']}\n"
        f"Rating: {resort['rating']}/5\n"
        f"Description: {resort['description']}\n"
        f"Amenities: {', '.join(resort['amenities'])}"
    )


def hapimag_get_resort_apartments(resort_id: int) -> str:
    """Get available apartments at a resort."""
    tool = HapimagGetResortApartmentsTool()
    result = tool.run(resort_id=resort_id)
    apartments = result["apartments"]

    if not apartments:
        return f"No apartments found for resort {resort_id}"

    output = f"Available apartments at resort {resort_id}:\n"
    for apt in apartments:
        output += (
            f"\n  {apt['name']} ({apt['type']})\n"
            f"    Max guests: {apt['max_guests']}, Size: {apt['size_sqm']}m²\n"
            f"    Amenities: {', '.join(apt['amenities'])}\n"
            f"    Price: {apt['price_per_night_points']} points/night\n"
        )
    return output


def hapimag_get_charging_station_for_resort(resort_id: int) -> str:
    """Get EV charging station information."""
    tool = HapimagGetChargingStationTool()
    result = tool.run(resort_id=resort_id)
    station = result["charging_station"]

    if not station.get("available", False):
        return station.get("message", "No charging station available")

    output = f"EV Charging at resort:\n"
    output += f"  Location: {station['location']}\n"
    output += f"  Pricing: {station['pricing']}\n"
    output += f"  Reservation required: {'Yes' if station['reservation_required'] else 'No'}\n"
    output += "  Chargers:\n"
    for charger in station["chargers"]:
        output += f"    - {charger['type']}: {charger['power_kw']}kW ({charger['count']}x) - {charger['status']}\n"
    return output


def hapimag_get_resort_gastronomy_details(resort_id: int, locale: str = "en_GB") -> str:
    """Get restaurant and dining information."""
    tool = HapimagGetGastronomyDetailsTool()
    result = tool.run(resort_id=resort_id, locale=locale)
    gastro = result["gastronomy"]

    if "error" in gastro:
        return gastro["error"]

    output = "Dining options:\n"

    if gastro.get("breakfast"):
        b = gastro["breakfast"]
        output += f"\nBreakfast: {'Included' if b['included'] else 'Not included'}\n"
        output += f"  Hours: {b['hours']}, Style: {b['style']}\n"

    for rest in gastro.get("restaurants", []):
        output += f"\nRestaurant: {rest['name']}\n"
        output += f"  Cuisine: {rest['cuisine']}\n"
        output += f"  Hours: {rest['hours']}\n"
        output += f"  Specialties: {', '.join(rest['specialties'])}\n"

    for bar in gastro.get("bars", []):
        output += f"\nBar: {bar['name']}\n"
        output += f"  Hours: {bar['hours']}\n"

    return output


def hapimag_get_activities_overview(resort_id: int, date_from: str, date_to: str, locale: str = "en_GB") -> str:
    """Get overview of available activities."""
    tool = HapimagGetActivitiesOverviewTool()
    result = tool.run(resort_id=resort_id, date_from=date_from, date_to=date_to, locale=locale)
    activities = result["activities"]

    if not activities:
        return f"No activities found for resort {resort_id}"

    output = f"Activities available ({date_from} to {date_to}):\n"
    for act in activities:
        dates = ", ".join(act["dates_available"][:3])
        output += (
            f"\n  {act['name']} [{act['category']}]\n"
            f"    Duration: {act['duration']}, Difficulty: {act['difficulty']}\n"
            f"    Price: CHF {act['price_chf']}\n"
            f"    Available: {dates}\n"
        )
    return output


def hapimag_get_activities_details(keys: List[str], date_from: str, date_to: str, locale: str = "en_GB") -> str:
    """Get detailed information about specific activities."""
    tool = HapimagGetActivitiesDetailsTool()
    result = tool.run(keys=keys, date_from=date_from, date_to=date_to, locale=locale)
    details = result["activity_details"]

    if not details:
        return "No activity details found for the specified keys"

    output = "Activity Details:\n"
    for detail in details:
        output += (
            f"\n{detail['name']}\n"
            f"  {detail['full_description']}\n"
            f"  Included: {', '.join(detail['included'])}\n"
            f"  What to bring: {', '.join(detail['what_to_bring'])}\n"
            f"  Meeting point: {detail['meeting_point']}\n"
            f"  Cancellation: {detail['cancellation_policy']}\n"
        )
    return output


def hapimag_get_resort_services(resort_id: int) -> str:
    """Get services available at a resort."""
    tool = HapimagGetResortServicesTool()
    result = tool.run(resort_id=resort_id)
    services = result["services"]

    if "error" in services:
        return services["error"]

    output = "Resort Services:\n"

    if services.get("reception"):
        r = services["reception"]
        output += f"\nReception: {r['hours']}\n"
        output += f"  Languages: {', '.join(r['languages'])}\n"

    if services.get("ski_storage"):
        s = services["ski_storage"]
        output += f"\nSki Storage: Available"
        if s.get("boot_dryer"):
            output += " (with boot dryer)"
        output += "\n"

    if services.get("shuttle_service"):
        sh = services["shuttle_service"]
        output += f"\nShuttle Service: {sh['schedule']}\n"
        output += f"  Destinations: {', '.join(sh['destinations'])}\n"

    return output


def hapimag_get_pet_charge(resort_id: int) -> str:
    """Get pet policy and charges."""
    tool = HapimagGetPetChargeTool()
    result = tool.run(resort_id=resort_id)
    pet = result["pet_policy"]

    if not pet.get("pets_allowed", False):
        return pet.get("message", "Pets not allowed")

    output = "Pet Policy:\n"
    output += f"  Charge: CHF {pet['charge_per_night_chf']}/night\n"
    output += f"  Max pets: {pet['max_pets']}\n"
    output += f"  Restrictions: {', '.join(pet['restrictions'])}\n"
    output += f"  Amenities: {', '.join(pet['amenities'])}\n"
    return output
