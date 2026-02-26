import os
import json
import asyncio
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# Setup ADK Runner for Evaluation
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from src.agents.smart_info_assistant.agent import smart_info_agent

async def run_agent(query: str, session_id: str) -> tuple[str, list[str]]:
    """Runs the agent and extracts the final text and any 'tool contexts' implicitly"""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=smart_info_agent,
        app_name="eval_app",
        session_service=session_service
    )
    
    await session_service.create_session(
        app_name="eval_app",
        user_id="eval_user",
        session_id=session_id
    )
    
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    final_response = ""
    contexts = []
    
    async for event in runner.run_async(user_id="eval_user", session_id=session_id, new_message=content):
        # We try to extract tool results as "contexts" for Ragas if possible
        if hasattr(event, "tool_results") and event.tool_results:
            for result in event.tool_results:
                if result.content and result.content.parts:
                    contexts.append(result.content.parts[0].text)
                    
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
            break
            
    # For ragas, we need at least some context if the tool was used.
    # Otherwise, fallback to the query itself if no context was retrieved (e.g. guardrail blocked).
    if not contexts:
        contexts = [final_response] 
        
    return final_response, contexts


async def run_evaluation():
    print("🚀 Starting LLM Task Evaluation Pipeline (World 2)")
    
    # Needs valid OPENAI_API_KEY for default Ragas evaluator model unless configured otherwise
    # Ragas primarily uses OpenAI internally for metrics computation out of the box. 
    if not os.getenv("OPENAI_API_KEY"):
         print("⚠️ WARNING: OPENAI_API_KEY is not set. Ragas uses OpenAI by default for its 'LLM-as-a-judge' metrics.")
         print("This script will attempt to proceed, but may fail during the 'evaluate' step.")
    
    # 1. Load Golden Dataset
    dataset_path = os.path.join(os.path.dirname(__file__), "golden_dataset.json")
    with open(dataset_path, "r") as f:
        golden_data = json.load(f)
        
    questions = []
    ground_truths = []
    answers = []
    contexts_list = []
    
    print("\n⏳ Generating answers from Smart Info Assistant...")
    # 2. Run Data through the Agent
    for i, item in enumerate(golden_data):
        q = item["question"]
        print(f"  [{i+1}/{len(golden_data)}] Processing: {q[:40]}...")
        
        # Call the agent
        # We use strict session isolation (different ID per query) to avoid state bleeding
        ans, contexts = await run_agent(q, session_id=f"eval_sess_{i}")
        
        questions.append(q)
        ground_truths.append(item["ground_truth"])
        answers.append(ans)
        contexts_list.append(contexts)
        
    # 3. Format for Ragas
    data = {"question": questions, "answer": answers, "contexts": contexts_list, "ground_truth": ground_truths}
    dataset = Dataset.from_dict(data)
    
    print("\n⚖️ Running probabilistic metrics (Faithfulness, Answer Relevancy) via Ragas...")
    # 4. Run Evaluation
    try:
        result = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
            ],
            raise_exceptions=False,
        )
        
        print("\n📊 Evaluation Results:")
        print(result)
        
        # Save report
        report_dir = os.path.join(os.path.dirname(__file__), "reports")
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "latest_eval.txt")
        with open(report_path, "w") as f:
            f.write(str(result))
        print(f"\n✅ Report written to {report_path}")
        
    except Exception as e:
        print(f"\n❌ Error during evaluation: {str(e)}")
        print("Hint: Did you set up the evaluator LLM API keys properly? (e.g. OPENAI_API_KEY)")


if __name__ == "__main__":
    asyncio.run(run_evaluation())
