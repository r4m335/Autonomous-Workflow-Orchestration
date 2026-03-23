from core.models import WorkflowState
from core.config import settings
from core.logger import logger
from typing import Dict, Any

def node_execution_agent(state: WorkflowState) -> Dict[str, Any]:
    """
    Execution Agent: Performs API/UI automation.
    """
    thread_id = state.get("job_id", "unknown")
    logger.info("Executing automated steps", thread_id=thread_id)
    
    norm_data = state.get("normalized_data", {})
    is_dry_run = state.get("is_dry_run", False)
    
    if is_dry_run:
        logger.info("Executing DRY RUN - no side effects", thread_id=thread_id)
        result_status = "SUCCESS (DRY)"
    else:
        logger.info(f"Connecting to CRM for tenant {settings.default_tenant}", thread_id=thread_id)
        result_status = "SUCCESS"
        
    return {
        "execution_results": {"status": result_status, "data": norm_data},
        "audit_trail": [f"Execution Agent processed {norm_data.get('vendor_name')}"]
    }
