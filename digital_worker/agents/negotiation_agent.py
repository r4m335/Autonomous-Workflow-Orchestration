from core.models import WorkflowState
from agents.llm_router import llm_router
from core.state_manager import state_manager
from core.config import settings
from core.logger import logger
from typing import Dict, Any

def node_negotiation_agent(state: WorkflowState) -> Dict[str, Any]:
    """
    Negotiation Agent: Handles price mismatches or logic disputes.
    """
    thread_id = state.get("job_id", "unknown")
    logger.info("Initiating negotiation subflow", thread_id=thread_id)
    
    norm_data = state.get("normalized_data", {})
    actual_amount = norm_data.get("amount", 0)
    target_amount = 1000.0 # Simulated PO amount
    
    diff = actual_amount - target_amount
    logger.info(f"Mismatch detected: {diff}", thread_id=thread_id)
    
    prompt = f"Invoice of {actual_amount} exceeds PO of {target_amount} by {diff}. Draft a professional dispute email."
    draft = llm_router.generate(prompt, tier="smart")
    
    state_manager.log_audit(
        thread_id=thread_id,
        agent_node="NegotiationAgent",
        action=f"Drafted dispute for price mismatch of {diff}"
    )
    
    return {
        "audit_trail": [f"Negotiation Agent drafted a dispute for amount mismatch: {diff}"],
        "current_action": {"type": "send_email", "draft": draft}
    }
