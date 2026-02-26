import os
from typing import Optional
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from src.agents.smart_info_assistant.sub_agents.weather_agent import weather_agent
from src.agents.smart_info_assistant.sub_agents.country_agent import country_agent
from src.agents.smart_info_assistant.sub_agents.currency_agent import currency_agent
from src.agents.smart_info_assistant.sub_agents.joke_agent import joke_agent

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Guardrail: Inspects the user's latest message. If it contains 'BLOCK',
    it intercepts and returns a predefined safety message without calling the LLM.
    """
    last_user_message = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                if content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    keyword = "BLOCK"
    if keyword in last_user_message.upper():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=f"[Guardrail Triggered] I cannot process this request because it contains the safety keyword: '{keyword}'.")]
            )
        )
    return None

smart_info_agent = Agent(
    name="smart_info_assistant",
    model=MODEL,
    description="Main coordinating agent for the Smart Info application. Routes to specialized experts.",
    instruction="""You are the Root Smart Info Assistant. Your role is to understand user requests and delegate them to the appropriate specialist in your team.
You have the following specialists:
1. 'weather_agent': Delegates requests about current weather conditions.
2. 'country_agent': Delegates requests about geographic/demographic facts of a country.
3. 'currency_agent': Delegates requests for live currency exchange rates.
4. 'joke_agent': Delegates requests for telling jokes or being entertained.

Analyze the user's request. If it matches a specialist's domain, automatically delegate to them.
If it doesn't match any specialist, respond politely that you can only help with weather, country info, currency, or jokes.
Do not attempt to answer factual questions directly if they belong to a specialist.""",
    sub_agents=[weather_agent, country_agent, currency_agent, joke_agent],
    before_model_callback=block_keyword_guardrail,
    output_key="last_smart_info_report"
)
