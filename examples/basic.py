"""
Basic example — define custom tool + run with LLM.
"""
from nano_tools import tool, ToolKit


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city (mock).
    city: City name to get weather for
    """
    return f"Weather in {city}: 28°C, sunny, humidity 65%"


@tool
def get_population(city: str) -> str:
    """Get population of a city (mock).
    city: City name to look up
    """
    populations = {"Jakarta": "10.6 million", "Surabaya": "2.9 million", "Bandung": "2.5 million"}
    return populations.get(city, f"Population data for {city} not available")


kit = ToolKit([get_weather, get_population])

print("Tool schemas:")
import json
for t in kit.list():
    print(json.dumps(t.schema, indent=2))

# Run with LLM (requires ANTHROPIC_API_KEY)
# result = kit.run_loop("What is the weather and population of Jakarta?")
# print(result)
