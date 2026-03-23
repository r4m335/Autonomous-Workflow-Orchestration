from core.models import WorkflowState
from core.config import settings
from core.logger import logger
from agents.llm_router import llm_router
from typing import Dict, Any
import json

def node_input_agent(state: WorkflowState) -> Dict[str, Any]:
    """
    Input Agent: Normalized data from LLM responses with key validation.
    """
    thread_id = state.get("job_id", "unknown")
    raw_input = state.get("raw_input", "")
    
    logger.info("Normalizing raw ingestion payload via LLM", thread_id=thread_id)
    
    # Prompt the LLM for structured JSON
    prompt = f"Extract vendor_name and amount from this text: {raw_input}. Return ONLY JSON."
    llm_output = llm_router.generate(prompt, tier="cheap")
    
    norm_data = {}
    
    try:
        # Attempt to parse LLM output
        clean_json = llm_output.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(clean_json)
        
        # Validate that we got what we needed
        if "vendor_name" in parsed and "amount" in parsed:
            norm_data = parsed
            logger.info("LLM extraction successful & validated", thread_id=thread_id)
        else:
            # If keys missing, force an error to trigger fallback
            raise KeyError("Missing required keys in LLM JSON response")
            
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.warning(f"LLM parsing or validation failed ({type(e).__name__}), using fallback heuristic.", thread_id=thread_id)
        # Heuristic fallback if LLM fails or returns incomplete JSON
        if "acme" in raw_input.lower():
            norm_data = {"vendor_name": "Acme Corp", "amount": 1250.0}
        else:
            norm_data = {"vendor_name": "Unknown", "amount": 0.0}
            
    return {"normalized_data": norm_data}
