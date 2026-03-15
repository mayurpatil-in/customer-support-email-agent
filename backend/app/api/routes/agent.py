from fastapi import APIRouter, HTTPException
from app.models.schemas import EmailRequest, EmailResponse
from app.agent.graph import agent_graph
from app.agent.state import AgentState

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/process-email", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    try:
        # Construct the initial state
        initial_state: AgentState = {
            "messages": [],
            "email_subject": request.subject,
            "email_body": request.body,
            "category": None,
            "kb_info": None,
            "draft_reply": None,
            "confidence": 0.0,
            "needs_human_review": False,
            "human_reviewed": False,
            "final_reply": None,
            "follow_up_scheduled": False
        }
        
        # Invoke LangGraph agent pipeline
        result = agent_graph.invoke(initial_state)
        
        # Map state variables to EmailResponse
        return EmailResponse(
            final_reply=result.get("final_reply", "Failed to generate reply."),
            category=result.get("category", "unknown"),
            confidence_score=result.get("confidence", 0.0),
            human_reviewed=result.get("human_reviewed", False),
            follow_up_scheduled=result.get("follow_up_scheduled", False)
        )
    except Exception as e:
        # Ideally, we should log the full traceback here for debugging.
        raise HTTPException(status_code=500, detail=str(e))
