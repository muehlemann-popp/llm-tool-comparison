"""Resort Amenities scenario - tests Hapimag and Maps tools."""

RESORT_QUERY = """
<context>\n## User Profile\n**Member ID** (member_id): 1530\nFirst name: Tomasz\nGender: male\n\n## Booking (Reservation) Details\n**Resort ID** (resort_id): 1\nResort Name: Andeer\nResort Location: unknown\n**Booking Number** (booking_id): 1768854650412\nArrival (check-in): 2026-02-02 (16:00)\nDeparture (check-out): 2026-02-21 (10:00)\nApartment Category: 2 room Comfort\n\n</context>

"<context>\n## Real-Time Data\n**Current Date and Time**: 2026-01-19 20:31\n**Booking Phase** (agent knowledge only): Pre-Arrival (Before trip)\n\nUser has not arrived yet, 315 hours (equals 13 days) remaining until arrival.\n\n\n</context>"

Provide resort amenities
"""

RESORT_SCENARIO_DESCRIPTION = """
Resort Amenities Scenario

This scenario tests the model's ability to:
- Interpret a vague, minimal user query
- Identify relevant tools to gather resort information
- Make multiple tool calls to build a comprehensive response
- Handle Hapimag resort APIs and Google Maps-style search

Expected Tool Calls (model should infer resort_id=1 or ask):
1. hapimag_get_resort_details(resort_id=1) - Get basic resort info
2. hapimag_get_resort_apartments(resort_id=1) - Get accommodation options
3. hapimag_get_resort_gastronomy_details(resort_id=1) - Get dining info
4. hapimag_get_resort_services(resort_id=1) - Get available services
5. hapimag_get_charging_station_for_resort(resort_id=1) - EV charging info
6. hapimag_get_pet_charge(resort_id=1) - Pet policy [optional]
7. maps_search_nearby_places(location, place_type) - Find nearby attractions [optional]

The model should synthesize information into a helpful overview of resort amenities.
"""
