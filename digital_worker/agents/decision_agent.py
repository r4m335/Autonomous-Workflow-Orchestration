from core.models import WorkflowState
from agents.llm_router import llm_router
from core.state_manager import state_manager

def node_decision_agent(state: WorkflowState) -> WorkflowState:
    """
    Decision Agent: Maps intent -> workflow graph (DAG).
    Dynamically generates the steps needed to fulfill the request.
    """
    print("--- [Decision Agent] Dynamic Workflow Generation ---")
    norm_data = state.get("normalized_data", {})
    
    # Route to smart model because this requires cross-system reasoning
    llm_router.generate(f"Determine intent for {norm_data}", tier="smart")
    
    # Simulated intent detection (Invoice vs Customer Support)
    intent = "invoice_processing"
    if "issue" in state.get("raw_input", "").lower():
        intent = "customer_support"
    
    # Dynamically generated DAG graph logic (simplified as a dict of tasks)
    generated_dag = {
        "tasks": [
            {"id": "t1", "system": "ERP", "action": "verify_po"},
            {"id": "t2", "system": "CRM", "action": "enter_invoice", "depends_on": ["t1"]}
        ]
    }
    
    state_manager.log_audit(
        thread_id=state.get("job_id", "unknown"),
        agent_node="DecisionAgent",
        action=f"Mapped intent to {intent} and generated sub-DAG."
    )
    
    return {
        "intent": intent,
        "dynamically_generated_dag": generated_dag
    }
