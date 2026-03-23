import sqlite3
import json
from typing import Dict, Any, List
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "digital_worker.db")

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Jobs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            workflow_name TEXT NOT NULL,
            status TEXT NOT NULL,  -- PENDING, RUNNING, COMPLETED, FAILED
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            context TEXT -- JSON storing overall job state/data
        )
    """)
    
    # Steps Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            step_name TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            status TEXT NOT NULL, -- PENDING, RUNNING, COMPLETED, FAILED
            input_data TEXT,
            output_data TEXT,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT,
            FOREIGN KEY(job_id) REFERENCES jobs(job_id)
        )
    """)
    
    # Audit Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL,
            step_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def create_job(job_id: str, workflow_name: str, initial_context: Dict[Any, Any] = None):
    conn = get_db()
    cursor = conn.cursor()
    context_str = json.dumps(initial_context or {})
    cursor.execute(
        "INSERT INTO jobs (job_id, workflow_name, status, context) VALUES (?, ?, ?, ?)",
        (job_id, workflow_name, "PENDING", context_str)
    )
    conn.commit()
    conn.close()

def log_audit(job_id: str, action: str, details: str = None, step_id: int = None):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO audit_logs (job_id, step_id, action, details) VALUES (?, ?, ?, ?)",
        (job_id, step_id, action, details)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Initialized database at {DB_PATH}")
