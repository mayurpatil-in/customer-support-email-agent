from langgraph.graph import StateGraph, START, END
from app.agent.state import AgentState
from app.agent.nodes import (
    categorize_email_node,
    search_knowledge_base_node,
    draft_reply_node,
    human_review_node,
    send_email_node
)

def should_route_to_human(state: AgentState):
    """
    Conditional edge function to determine if the drafted reply
    needs to be sent to human review before sending.
    """
    if state.get("needs_human_review"):
        return "human_review"
    return "send_email"

def build_graph():
    workflow = StateGraph(AgentState)

    # 1. Add all nodes to the graph
    workflow.add_node("categorize_email", categorize_email_node)
    workflow.add_node("search_kb", search_knowledge_base_node)
    workflow.add_node("draft_reply", draft_reply_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("send_email", send_email_node)

    # 2. Add edges to connect the nodes (linear path)
    workflow.add_edge(START, "categorize_email")
    workflow.add_edge("categorize_email", "search_kb")
    workflow.add_edge("search_kb", "draft_reply")

    # 3. Add Conditional Edges
    # After drafting, decide whether to send directly or route to human
    workflow.add_conditional_edges(
        "draft_reply",
        should_route_to_human,
        {
            "human_review": "human_review",
            "send_email": "send_email",
        }
    )

    # 4. Finalizing edges
    workflow.add_edge("human_review", "send_email")
    workflow.add_edge("send_email", END)

    # Compile the graph
    app = workflow.compile()
    
    return app

agent_graph = build_graph()
