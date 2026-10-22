import sqlite3
from datetime import datetime

DB_FILE = "audit_log.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                client_id TEXT NOT NULL,
                action TEXT NOT NULL,
                decision TEXT NOT NULL,
                reason TEXT NOT NULL
            )
        """)
        conn.commit()

def log_event(client_id: str, action: str, decision: str, reason: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO audit_logs (timestamp, client_id, action, decision, reason) VALUES (?, ?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), client_id, action, decision, reason)
        )
        conn.commit()