from core.models import WorkflowState
from core.state_manager import state_manager
from core.logger import logger
from typing import Dict, Any

def node_exception_agent(state: WorkflowState) -> Dict[str, Any]:
    """
    Exception Agent: Handles anomalies, self-healing, and human escalation.
    """
    thread_id = state.get("job_id", "unknown")
    exceptions = state.get("exceptions", [])
    
    logger.error(f"Exceptions encountered: {exceptions}", thread_id=thread_id)
    
    # Logic to decide if we can self-heal or need human help
    if len(exceptions) < 3:
        action = "Attempting self-healing retry"
        logger.info("Retrying under self-healing policy", thread_id=thread_id)
    else:
        action = "Escalating to Human-in-the-loop Queue"
        logger.warning("Max retries exceeded. Manual intervention required.", thread_id=thread_id)
    
    state_manager.log_audit(
        thread_id=thread_id,
        agent_node="ExceptionAgent",
        action=action
    )
    
    return {
        "audit_trail": [f"Exception Agent: {action}"],
        "status": "waiting_for_human" if len(exceptions) >= 3 else "retrying"
    }
