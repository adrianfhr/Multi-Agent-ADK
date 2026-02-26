import pytest
import asyncio
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from src.agents.smart_info_assistant.agent import smart_info_agent

@pytest.mark.asyncio
async def test_guardrail_block():
    """
    Test that the guardrail intercepts 'BLOCK' keyword and prevents LLM processing.
    This is an integration test of the agent framework without calling the actual LLM.
    """
    session_service = InMemorySessionService()
    runner = Runner(
        agent=smart_info_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    await session_service.create_session(
        app_name="test_app",
        user_id="test_user",
        session_id="session_1"
    )
    
    content = types.Content(role='user', parts=[types.Part(text="Please BLOCK this request")])
    
    final_response = ""
    async for event in runner.run_async(user_id="test_user", session_id="session_1", new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            break
            
    assert "[Guardrail Triggered]" in final_response
    assert "BLOCK" in final_response
