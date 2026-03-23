import pytest
import uuid
from core.dag_engine import dag_app

def test_negotiation_loop():
    """Verifies the negotiation branch triggers correctly for mismatches."""
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_input = {
        "job_id": thread_id,
        "tenant_id": "tenant_a",
        "is_dry_run": True,
        "raw_input": "FWD: Invoice mismatch. Acme Corp billed $1250 but PO was $1000.",
        "exceptions": [],
        "audit_trail": []
    }
    
    # Run the graph
    events = []
    for event in dag_app.stream(initial_input, config, stream_mode="values"):
        events.append(event)
             
    final_state = dag_app.get_state(config)
    
    # Assertions
    assert final_state.values.get("validation_score") is not None
    score = final_state.values.get("validation_score")
    assert 0.5 < score < 0.8 # Range that triggers negotiation
    
    # Check if NegotiationAgent was hit
    found_neg = any("Negotiation Agent" in log for log in final_state.values.get("audit_trail", []))
    assert found_neg, "Negotiation Agent should be triggered for amount mismatch"
