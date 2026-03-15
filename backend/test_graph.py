from dotenv import load_dotenv
import json

# Load environment variables first
load_dotenv()

from app.agent.graph import agent_graph
from app.agent.state import AgentState

def test_agent():
    # Test 1: A general billing request
    print("--- TEST 1: BILLING REQUEST ---")
    initial_state_1: AgentState = {
        "messages": [],
        "email_subject": "Refund request",
        "email_body": "Can I get a refund for my last purchase? It's been 3 days since I bought it.",
        "category": None,
        "kb_info": None,
        "draft_reply": None,
        "confidence": 0.0,
        "needs_human_review": False,
        "human_reviewed": False,
        "final_reply": None,
        "follow_up_scheduled": False
    }

    result_1 = agent_graph.invoke(initial_state_1)
    print(f"Category: {result_1.get('category')}")
    print(f"Draft Reply: {result_1.get('draft_reply')}")
    print(f"Final Reply: {result_1.get('final_reply')}")
    print(f"Needs Human Review: {result_1.get('needs_human_review')}")
    print("\n")

    # Test 2: A complex complaint
    print("--- TEST 2: COMPLEX COMPLAINT ---")
    initial_state_2: AgentState = {
        "messages": [],
        "email_subject": "Extremely angry customerrr",
        "email_body": "Your service is TERRIBLE. I demand to speak to your manager right now! Nothing works, everything is broken. If no one fixes this in 5 minutes I am suing you.",
        "category": None,
        "kb_info": None,
        "draft_reply": None,
        "confidence": 0.0,
        "needs_human_review": False,
        "human_reviewed": False,
        "final_reply": None,
        "follow_up_scheduled": False
    }

    result_2 = agent_graph.invoke(initial_state_2)
    print(f"Category: {result_2.get('category')}")
    print(f"Draft Reply: {result_2.get('draft_reply')}")
    print(f"Final Reply: {result_2.get('final_reply')}")
    print(f"Needs Human Review: {result_2.get('needs_human_review')}")
    print(f"Human Reviewed: {result_2.get('human_reviewed')}")

if __name__ == "__main__":
    test_agent()
