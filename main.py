import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from src.agents.smart_info_assistant.agent import smart_info_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

async def interactive_shell():
    print("=====================================================")
    print("🤖 Welcome to Smart Info Assistant (Google ADK Demo)")
    print("=====================================================")
    print("Features:")
    print(" 🌤️  Ask about weather (e.g., 'What is the weather in Tokyo?')")
    print(" 🌍  Ask about countries (e.g., 'Tell me about Brazil')")
    print(" 💱  Convert currency (e.g., '100 USD to EUR')")
    print(" 😄  Ask for a joke (e.g., 'Tell me a programming joke')")
    print(" 🛡️  Guardrail Demo (Type 'BLOCK this message')")
    print("Type 'exit' or 'quit' to stop.")
    print("=====================================================\n")

    session_service = InMemorySessionService()
    runner = Runner(
        agent=smart_info_agent,
        app_name="smart_info_app",
        session_service=session_service
    )
    
    user_id = "demo_user"
    session_id = "session_001"
    
    await session_service.create_session(
        app_name="smart_info_app",
        user_id=user_id,
        session_id=session_id
    )

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            if not user_input.strip():
                continue
                
            content = types.Content(role='user', parts=[types.Part(text=user_input)])
            
            final_response = "..."
            async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response = event.content.parts[0].text
                    elif event.actions and event.actions.escalate:
                        final_response = f"Error: {event.error_message}"
                    break
                    
            print(f"\n🤖 Assistant: {final_response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def main():
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️ Warning: GOOGLE_API_KEY is not set. The agent will likely fail unless using a local LiteLLM proxy.")
        
    try:
        asyncio.run(interactive_shell())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
