from core.models import WorkflowState
from agents.llm_router import llm_router
from core.state_manager import state_manager

def node_negotiation_agent(state: WorkflowState) -> WorkflowState:
    """
    Negotiation Agent (Requirement #12):
    Specialized for "Accounts Assistant" roles. Handles price mismatches 
    or logic disputes by drafting counter-offer emails.
    """
    print("--- [Negotiation Agent] Handling Price Mismatch ---")
    
    norm_data = state.get("normalized_data", {})
    # Simulation: We assume a 'target_price' exists in context for reconciliation
    actual_amount = norm_data.get("amount", 0)
    target_amount = 1000.0 # Simulated PO amount
    
    diff = actual_amount - target_amount
    
    prompt = f"Invoice of {actual_amount} exceeds PO of {target_amount} by {diff}. Draft a professional dispute email."
    
    # Use 'smart' model for behavioral negotiation
    draft = llm_router.generate(prompt, tier="smart")
    
    # Audit transition
    state_manager.log_audit(
        thread_id=state.get("job_id", "unknown"),
        agent_node="NegotiationAgent",
        action=f"Drafted dispute for price mismatch of {diff}"
    )
    
    # Append to audit trail for frontend
    return {
        "audit_trail": [f"Negotiation Agent drafted a dispute for amount mismatch: {diff}"],
        "current_action": {"type": "send_email", "draft": "Dear Vendor, your invoice exceeds our PO..."}
    }
