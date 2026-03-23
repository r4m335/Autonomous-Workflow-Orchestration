from core.models import WorkflowState
from core.config import settings
from core.logger import logger
from typing import Dict, Any

def node_input_agent(state: WorkflowState) -> Dict[str, Any]:
    """
    Input Agent: Normalizes messy data into structured schema.
    """
    thread_id = state.get("job_id", "unknown")
    raw_input = state.get("raw_input", "")
    
    logger.info("Normalizing raw ingestion payload", thread_id=thread_id)
    
    # Simulation: Extracting basic details from messy text
    # In production, this would use OCR/LLM
    norm_data = {"vendor_name": "Acme Corp", "amount": 1250.0}
    
    if "1250" in raw_input:
        norm_data["amount"] = 1250.0
        
    logger.info(f"Targeting tenant: {settings.default_tenant}", thread_id=thread_id)
        
    return {"normalized_data": norm_data}
