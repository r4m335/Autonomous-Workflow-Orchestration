import sqlite3
from typing import Optional, Dict, Any, List
from datetime import datetime
from langgraph.checkpoint.memory import MemorySaver
from core.config import settings

class StateManager:
    """
    Manages deterministic checkpoints for LangGraph DAGs.
    Provides methods to retrieve the active checkpointer and interact 
    with the underlying database for audit trails.
    """
    def __init__(self, db_path: str = None):
        self.db_path = db_path or settings.db_path
        # Use MemorySaver for local dev, can be swapped to SqliteSaver
        self.checkpointer = MemorySaver()
        self._init_audit_db()

    def _init_audit_db(self):
        """Initializes a separate table for human-readable audit trails and SLA metrics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workflow_audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT NOT NULL,
                agent_node TEXT NOT NULL,
                action TEXT NOT NULL,
                confidence REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def get_checkpointer(self):
        """Return the LangGraph checkpointer instance."""
        return self.checkpointer

    def log_audit(self, thread_id: str, agent_node: str, action: str, confidence: Optional[float] = None):
        """Record an immutable audit log for compliance and pattern mining."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workflow_audit (thread_id, agent_node, action, confidence) VALUES (?, ?, ?, ?)",
            (thread_id, agent_node, action, confidence)
        )
        conn.commit()
        conn.close()

# Singleton instance
state_manager = StateManager()
