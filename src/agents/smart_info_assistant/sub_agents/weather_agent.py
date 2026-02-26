import os
from google.adk.agents import Agent
from src.agents.tools.info_tools import get_weather

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

weather_agent = Agent(
    name="weather_agent",
    model=MODEL,
    description="Provides current weather, temperature, humidity, and wind speed for any city around the world.",
    instruction="""You are the Weather Specialist Agent. Your ONLY task is to provide real-time weather information.
Use the 'get_weather' tool when the user asks for the weather in a specific city.
If the tool returns an error (e.g., city not found), inform the user politely.
If successful, present the weather report clearly and concisely. Do not attempt to answer non-weather questions.""",
    tools=[get_weather]
)
