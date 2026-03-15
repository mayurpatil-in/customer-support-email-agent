from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.agent.state import AgentState
from app.models.schemas import EmailCategory, DraftResponse
from app.core.config import settings
from app.core.vectorstore import search_documents
import logging

logger = logging.getLogger(__name__)

# Initialize the LLM (Requires OPENAI_API_KEY in .env)
# Using a lightweight model for categorization, and a better one for drafting if desired.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def categorize_email_node(state: AgentState) -> dict:
    """Classifies the intent and category of the incoming email."""
    logger.info("--- CATEGORIZING EMAIL ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert customer support routing agent. "
                   "Classify the incoming customer email into a specific category and determine its urgency. "
                   "Categories could be: 'billing', 'technical_support', 'general_inquiry', 'complaint', or 'other'."),
        ("user", "Subject: {subject}\n\nBody: {body}")
    ])
    
    chain = prompt | llm.with_structured_output(EmailCategory)
    result: EmailCategory = chain.invoke({
        "subject": state["email_subject"],
        "body": state["email_body"]
    })
    
    return {"category": result.category}

def search_knowledge_base_node(state: AgentState) -> dict:
    """
    Searches the FAISS vector store for relevant information.
    """
    logger.info("--- SEARCHING KNOWLEDGE BASE ---")
    
    # Construct a search query. We can use the category, subject, and body for max context.
    category = state.get("category", "")
    subject = state.get("email_subject", "")
    body = state.get("email_body", "")
    
    search_query = f"Category: {category}\nSubject: {subject}\nBody: {body}"
    
    # Hit the local FAISS DB for top 2 closest documents
    kb_info = search_documents(search_query, k=2)
        
    return {"kb_info": kb_info}

def draft_reply_node(state: AgentState) -> dict:
    """Drafts an appropriate response to the customer based on context."""
    logger.info("--- DRAFTING REPLY ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and empathetic customer support agent. "
                   "Draft a polite and professional reply to the customer's email. "
                   "Use the information retrieved from our knowledge base to answer perfectly. "
                   "If the question is too complex, emotional, or not fully answered by the KB, set 'needs_human_review' to true.\n"
                   "Knowledge Base Context:\n{kb_info}"),
        ("user", "Customer Email Subject: {subject}\n\nCustomer Email Body: {body}")
    ])
    
    chain = prompt | llm.with_structured_output(DraftResponse)
    result: DraftResponse = chain.invoke({
        "subject": state["email_subject"],
        "body": state["email_body"],
        "kb_info": state.get("kb_info", "No additional context.")
    })
    
    return {
        "draft_reply": result.draft,
        "confidence": result.confidence,
        "needs_human_review": result.needs_human_review
    }

def human_review_node(state: AgentState) -> dict:
    """
    Sends complex or urgent cases for human review.
    In a real system, this might pause execution (via interrupts in LangGraph v0.1+) 
    or just flag it for an external dashboard.
    For this scaffold, we simulate a human modifying the reply.
    """
    logger.info("--- HUMAN REVIEW NEEDED ---")
    
    draft = state.get("draft_reply", "")
    
    # Simulated human edit
    reviewed_reply = f"[HUMAN REVIEWED & APPROVED] {draft}"
    
    return {
        "draft_reply": reviewed_reply,
        "human_reviewed": True
    }

def send_email_node(state: AgentState) -> dict:
    """
    Sends the final reply to the customer and determines if a follow-up is needed.
    """
    logger.info("--- FINALIZING AND SENDING EMAIL ---")
    
    final_reply = state.get("draft_reply", "We apologize, but we could not process your request at this time.")
    human_reviewed = state.get("human_reviewed", False)
    
    # Simple logic to schedule a follow up if human interaction was needed
    follow_up = True if human_reviewed else False
    
    # In a real app, integrate SES/SendGrid/SMTP here to actually dispatch the email
    logger.info(f"Email Sent! Follow-up scheduled: {follow_up}")
    
    return {
        "final_reply": final_reply,
        "follow_up_scheduled": follow_up
    }
