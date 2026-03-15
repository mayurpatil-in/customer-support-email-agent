import operator
from typing import Annotated, TypedDict
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    """The state of the email processing agent."""
    messages: Annotated[list[AnyMessage], operator.add]
    email_subject: str
    email_body: str
    
    # State defined throughout the flow
    category: str | None
    kb_info: str | None
    
    # Drafting & Review
    draft_reply: str | None
    confidence: float
    needs_human_review: bool
    human_reviewed: bool
    
    # Finalization
    final_reply: str | None
    follow_up_scheduled: bool
