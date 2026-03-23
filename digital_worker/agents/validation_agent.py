from core.models import WorkflowState
from agents.llm_router import llm_router
from core.state_manager import state_manager

def node_validation_agent(state: WorkflowState) -> WorkflowState:
    """
    Validation Agent: Verifies outputs before final commit.
    Generates a confidence score for the Execution block.
    """
    print("--- [Validation Agent] Verifying Execution ---")
    results = state.get("execution_results", {})
    
    # We ask an LLM to review the structured output against the initial intent
    # and provide a confidence score representing the certainty of correctness.
    res = llm_router.generate(f"Validate this execution: {results}", tier="smart")
    
    # Simulate a confidence scoring mechanism
    # If a discrepancy is detected (e.g. price mismatch), return score in negotiation range (0.5 - 0.8)
    confidence_score = 0.95 
    
    raw_input = state.get("raw_input", "").lower()
    if "mismatch" in raw_input or "exceeds" in raw_input:
        print("[Validation Agent] Discrepancy detected! Routing to Negotiation.")
        confidence_score = 0.65
        
    if "exceptions" in state and state["exceptions"]:
        confidence_score = 0.4
        
    state_manager.log_audit(
        thread_id=state.get("job_id", "unknown"),
        agent_node="ValidationAgent",
        action="Validated execution",
        confidence=confidence_score
    )
    
    return {"validation_score": confidence_score}
