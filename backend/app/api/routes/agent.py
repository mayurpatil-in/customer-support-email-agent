from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.models.schemas import EmailRequest, EmailResponse
from app.agent.graph import agent_graph
from app.agent.state import AgentState
from app.db.database import save_processed_email, get_all_emails, get_email_by_id

# Extended Request to handle customer_email
class DashboardEmailRequest(EmailRequest):
    customer_email: str = Field(..., description="The sender email address")

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/process-email", response_model=EmailResponse)
async def process_email(request: DashboardEmailRequest):
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
        
        # Format the processed data for our database
        processed_data = {
            "customer_email": request.customer_email,
            "subject": request.subject,
            "body": request.body,
            "category": result.get("category", "unknown"),
            "kb_info": result.get("kb_info", ""),
            "draft_reply": result.get("draft_reply", ""),
            "needs_human_review": result.get("needs_human_review", False),
            "human_reviewed": result.get("human_reviewed", False),
            "final_reply": result.get("final_reply", "")
        }
        
        # Save to SQLite
        try:
             save_processed_email(processed_data)
        except Exception as db_e:
             # Just log it for now, let the API return the result
             print(f"Error saving to DB: {db_e}")
        
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

@router.get("/inbox")
async def get_inbox():
    """Retrieve all historically processed emails for the dashboard."""
    try:
        emails = get_all_emails()
        return {"emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/email/{email_id}")
async def get_email_details(email_id: int):
    """Retrieve details for a specific processed email."""
    try:
        email = get_email_by_id(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        return dict(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
