import os
from google.adk.agents import Agent
from src.agents.tools.info_tools import get_joke

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

joke_agent = Agent(
    name="joke_agent",
    model=MODEL,
    description="Provides random jokes or punchlines to entertain the user. Use this when the user asks to hear a joke or be entertained.",
    instruction="""You are the Entertainment & Joke Specialist Agent. Your ONLY task is to tell jokes.
Use the 'get_joke' tool to fetch a random joke when the user explicitly asks for one.
Present the joke exactly as returned. Add a small funny emoji at the end.""",
    tools=[get_joke]
)
