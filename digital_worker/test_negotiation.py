import uuid
from core.dag_engine import dag_app

def test_negotiation_loop():
    print("--- [Test] Triggering Negotiation Loop ---")
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Input that triggers the "mismatch" logic in ValidationAgent
    initial_input = {
        "job_id": thread_id,
        "tenant_id": "tenant_a",
        "is_dry_run": True,
        "raw_input": "FWD: Invoice mismatch. Acme Corp billed $1250 but PO was $1000.",
        "exceptions": [],
        "audit_trail": []
    }
    
    print(f"Executing Thread: {thread_id}")
    
    for event in dag_app.stream(initial_input, config, stream_mode="values"):
        if "audit_trail" in event and event["audit_trail"]:
             print(f"Log: {event['audit_trail'][-1]}")
             
    final_state = dag_app.get_state(config)
    print(f"\nFinal Intent: {final_state.values.get('intent')}")
    print(f"Final Score: {final_state.values.get('validation_score')}")
    
    # Check if NegotiationAgent was hit
    found_neg = any("Negotiation Agent" in log for log in final_state.values.get("audit_trail", []))
    if found_neg:
        print("SUCCESS: Negotiation Agent was successfully triggered!")
    else:
        print("FAILURE: Negotiation Agent was NOT triggered.")

if __name__ == "__main__":
    test_negotiation_loop()
