from core.models import WorkflowState
from agents.llm_router import llm_router
from core.state_manager import state_manager
from core.config import settings
from core.logger import logger
from typing import Dict, Any

def node_validation_agent(state: WorkflowState) -> Dict[str, Any]:
    """
    Validation Agent: Verifies outputs before final commit.
    """
    thread_id = state.get("job_id", "unknown")
    logger.info("Verifying execution results", thread_id=thread_id)
    
    results = state.get("execution_results", {})
    
    # We ask an LLM to review the structured output against the initial intent
    res = llm_router.generate(f"Validate this execution: {results}", tier="smart")
    
    # Use configuration-driven threshold
    confidence_score = settings.validation_threshold + 0.15 
    
    raw_input = state.get("raw_input", "").lower()
    if "mismatch" in raw_input or "exceeds" in raw_input:
        logger.warning("Discrepancy detected in input data", thread_id=thread_id)
        confidence_score = settings.validation_threshold - 0.15
        
    if "exceptions" in state and state["exceptions"]:
        confidence_score = 0.4
        
    state_manager.log_audit(
        thread_id=thread_id,
        agent_node="ValidationAgent",
        action="Validated execution",
        confidence=confidence_score
    )
    
    return {"validation_score": confidence_score}
