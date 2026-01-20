"""Travel Research Assistant scenario definition."""

TRAVEL_QUERY = """I'm planning a 5-day trip to Tokyo in April. Can you help me plan this?

I need to know:
1. What's the weather like in Tokyo in April?
2. Can you find good hotels under $200/night near Shibuya?
3. What are the must-see attractions I should visit?
4. Can you suggest a 3-day itinerary based on the attractions?

Also, if you have time, let me know about transportation options from the airport and how much $200 USD is in Japanese Yen."""

TRAVEL_SCENARIO_DESCRIPTION = """
Travel Research Assistant Scenario

This scenario tests the model's ability to:
- Understand a complex multi-part query
- Identify which tools to call and in what order
- Handle 3-4 tool calls to gather comprehensive information
- Synthesize information from multiple sources into a coherent response
- Provide practical, actionable travel recommendations

Expected Tool Calls:
1. get_weather_forecast(location="Tokyo", month="April")
2. search_hotels(city="Tokyo", area="Shibuya", max_price=200)
3. find_attractions(city="Tokyo")
4. convert_currency(amount=200, from_currency="USD", to_currency="JPY") [optional]
5. get_transportation_info(city="Tokyo") [optional]

The model should create a structured itinerary using the gathered information.
"""
