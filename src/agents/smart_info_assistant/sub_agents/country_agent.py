import os
from google.adk.agents import Agent
from src.agents.tools.info_tools import get_country_info

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

country_agent = Agent(
    name="country_agent",
    model=MODEL,
    description="Provides basic geographic and demographic information about specific countries (capital, region, population).",
    instruction="""You are the Country Information Specialist Agent. Your ONLY task is to provide details about a country.
Use the 'get_country_info' tool when the user asks for facts about a country like its capital, population, or region.
If the tool returns an error, cleanly relay the message to the user.
If successful, present the information naturally. Do not attempt to answer non-country questions.""",
    tools=[get_country_info]
)
