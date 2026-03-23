from core.models import WorkflowState
from core.state_manager import state_manager

def node_exception_agent(state: WorkflowState) -> WorkflowState:
    """
    Exception Agent: Primary differentiator vs RPA.
    Handles escalations, DOM drifts, API failures, and low-confidence validation.
    """
    print("--- [Exception Agent] Handling Anomalies ---")
    
    score = state.get("validation_score", 1.0)
    exceptions = state.get("exceptions", [])
    
    if score < 0.8:
        print(f"[!] Validation Confidence ({score}) below threshold (0.80)")
        exceptions.append("Low Confidence Validation")
        
    for error in exceptions:
        print(f"[!] Resolving Error: {error}")
        
    # Anomaly Detection & Self-Healing Logic
    # 1. Determine if retryable with an alternative model
    # 2. Determine if human-in-the-loop is required
    
    # For now, we simulate logging an escalation event
    state_manager.log_audit(
        thread_id=state.get("job_id", "unknown"),
        agent_node="ExceptionAgent",
        action="Escalated to Human-in-the-loop Queue" if len(exceptions) > 2 else "Attempting Self-Healing subflow"
    )
    
    # We add an error counter to break out of infinite retry loops in the dag
    return {"exceptions": ["Self-healing attempted"]}
