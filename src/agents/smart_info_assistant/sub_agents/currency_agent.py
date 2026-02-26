import os
from google.adk.agents import Agent
from src.agents.tools.info_tools import get_exchange_rate

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

currency_agent = Agent(
    name="currency_agent",
    model=MODEL,
    description="Provides live currency exchange rates between two 3-letter currency codes (e.g., USD to IDR or EUR to JPY).",
    instruction="""You are the Currency Exchange Specialist Agent. Your ONLY task is to provide live exchange rates.
Use the 'get_exchange_rate' tool when the user asks for currency conversion.
Make sure you extract the 3-letter currency codes correctly from the user's query (e.g., 'US Dollars' -> 'USD', 'Rupiah' -> 'IDR').
If the tool errors, inform the user politely. If successful, present the conversion rate clearly.""",
    tools=[get_exchange_rate]
)
