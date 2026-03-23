import uuid
from core.dag_engine import dag_app
from core.state_manager import state_manager
import sqlite3
import pandas as pd

def print_break(title: str):
    print(f"\n{'='*20} {title.upper()} {'='*20}")

def test_adaptive_dag():
    print_break("Initializing Workflow")
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Intentionally messy, partial data snippet
    initial_input = {
        "job_id": thread_id,
        "tenant_id": "tenant_a",
        "is_dry_run": False, # Setting to False triggers the browser and API fallbacks
        "raw_input": "FWD: Need this processed ASAP. Acmee Corppp, $1250... wait maybe it's 1250.00? Date missing.",
        "exceptions": [],
        "audit_trail": []
    }
    
    print(f"Triggering Execution for Thread: {thread_id}")
    
    # Run the graph
    events = []
    for event in dag_app.stream(initial_input, config, stream_mode="values"):
        events.append(event)
        
    print_break("Final State Reached")
    final_state = dag_app.get_state(config)
    print(f"Intent detected: {final_state.values.get('intent')}")
    print(f"Exceptions caught: {final_state.values.get('exceptions')}")
    print(f"Validation Score: {final_state.values.get('validation_score')}")
    
    print_break("Audit Trail (SQLite Verification)")
    conn = sqlite3.connect("digital_worker_state.db")
    df = pd.read_sql_query(f"SELECT * FROM workflow_audit WHERE thread_id='{thread_id}' ORDER BY timestamp", conn)
    print(df.to_string())
    conn.close()

if __name__ == "__main__":
    test_adaptive_dag()
