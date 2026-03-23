import pytest
import uuid
import sqlite3
import pandas as pd
from core.dag_engine import dag_app

def test_adaptive_dag(temp_db):
    """Verifies DAG resilience under messy input constraints."""
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_input = {
        "job_id": thread_id,
        "tenant_id": "tenant_a",
        "is_dry_run": True,
        "raw_input": "FWD: Need this processed ASAP. Acmee Corppp, $1250... wait maybe it's 1250.00? Date missing.",
        "exceptions": [],
        "audit_trail": []
    }
    
    # Run the graph
    events = []
    for event in dag_app.stream(initial_input, config, stream_mode="values"):
        events.append(event)
        
    final_state = dag_app.get_state(config)
    
    # Assertions
    assert final_state.values.get("intent") is not None
    assert "exceptions" in final_state.values
    
    # Verify audit trail extraction logic
    audit = final_state.values.get("audit_trail", [])
    assert len(audit) > 0
