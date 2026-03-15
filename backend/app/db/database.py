import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "./data/emails.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_email TEXT,
                subject TEXT,
                body TEXT,
                category TEXT,
                kb_info TEXT,
                draft_reply TEXT,
                needs_human_review BOOLEAN,
                human_reviewed BOOLEAN,
                final_reply TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def save_processed_email(email_data: dict) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO emails (
                customer_email, subject, body, category, 
                kb_info, draft_reply, needs_human_review, 
                human_reviewed, final_reply
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            email_data.get("customer_email"),
            email_data.get("subject"),
            email_data.get("body"),
            email_data.get("category"),
            email_data.get("kb_info"),
            email_data.get("draft_reply"),
            email_data.get("needs_human_review", False),
            email_data.get("human_reviewed", False),
            email_data.get("final_reply")
        ))
        conn.commit()
        return cursor.lastrowid

def get_all_emails() -> list[dict]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM emails ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_email_by_id(email_id: int) -> dict | None:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM emails WHERE id = ?', (email_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
