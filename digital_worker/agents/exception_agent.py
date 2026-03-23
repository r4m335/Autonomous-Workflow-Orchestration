from core.models import WorkflowState
from core.state_manager import state_manager
from core.logger import logger
from typing import Dict, Any

def node_exception_agent(state: WorkflowState) -> Dict[str, Any]:
    """
    Exception Agent: Correctly accumulates anomalies without overwriting the list.
    """
    thread_id = state.get("job_id", "unknown")
    # Correctly build on existing exceptions
    existing_exceptions = state.get("exceptions", [])
    new_exception = "Anomaly detected: validation score below threshold"
    
    updated_exceptions = existing_exceptions + [new_exception]
    
    logger.error(f"Exceptions accumulated: {len(updated_exceptions)}", thread_id=thread_id)
    
    if len(updated_exceptions) < 3:
        action = "Attempting self-healing retry"
    else:
        action = "Escalating to Human-in-the-loop Queue"
        logger.warning("Max retries reached", thread_id=thread_id)
    
    state_manager.log_audit(
        thread_id=thread_id,
        agent_node="ExceptionAgent",
        action=action
    )
    
    return {
        "exceptions": updated_exceptions,
        "audit_trail": [f"Exception Agent: {action}"],
        "status": "waiting_for_human" if len(updated_exceptions) >= 3 else "retrying"
    }
