import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

from app.core.vectorstore import create_and_save_vector_store
from langchain_core.documents import Document

def init_db():
    print("Initializing FAISS Vector Store with dummy documents...")

    # Dummy E-commerce / Tech Support Policies
    docs = [
        Document(
            page_content="Policy: Returns and Refunds. Customers can return most items within 30 days of receipt of delivery for a full refund. Refunds to credit cards take 5-7 business days to process after the item is received at our facility. Return shipping may be deducted unless the item was defective.",
            metadata={"source": "returns_policy", "category": "billing"}
        ),
        Document(
            page_content="Policy: Defective Item Replacement. If a customer receives a defective item, they must report it within 14 days. We will issue a prepaid return label and instantly ship a replacement upon return package scan.",
            metadata={"source": "defective_items", "category": "billing"}
        ),
        Document(
            page_content="Tech Support Guide: Password Reset. To reset an account password, direct the user to click the 'Forgot Password' link on the login page. An email with a reset link will be sent. The link expires in 2 hours. If they don't receive it, ask them to check their spam folder.",
            metadata={"source": "password_reset", "category": "technical_support"}
        ),
        Document(
            page_content="Tech Support Guide: Website Loading Issues. If the customer complains about the website being slow or not loading properly, advise them to clear their browser cache and cookies, or try accessing the site in Incognito/Private browsing mode. Supported browsers include the latest versions of Chrome, Firefox, Safari, and Edge.",
            metadata={"source": "loading_issues", "category": "technical_support"}
        ),
        Document(
            page_content="General Info: Customer Support Hours. Our live customer support agents are available Monday through Friday, from 9:00 AM to 6:00 PM Eastern Standard Time (EST). During off-hours, emails are placed in a queue and answered the following business day.",
            metadata={"source": "support_hours", "category": "general_inquiry"}
        ),
        Document(
            page_content="Policy: Warranty Information. All electronics come with a standard 1-year manufacturer's warranty covering hardware defects under normal use. Accidental damage (drops, spills) is NOT covered unless the customer purchased the 'Accident Protection Plan'.",
            metadata={"source": "warranty_policy", "category": "general_inquiry"}
        ),
    ]

    create_and_save_vector_store(docs)
    print("FAISS database successfully created and saved locally!")

if __name__ == "__main__":
    init_db()
