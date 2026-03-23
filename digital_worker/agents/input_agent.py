from core.models import WorkflowState
from agents.llm_router import llm_router
from core.state_manager import state_manager
import json

def node_input_agent(state: WorkflowState) -> WorkflowState:
    """
    Input Agent: Parses emails, PDFs, attachments using OCR + semantic extraction.
    """
    print("--- [Input Agent] Processing Input ---")
    raw_input = state.get("raw_input", "")
    
    # Simulate Tesseract OCR + Layout models if PDF, 
    # Use cheap LLM to parse text into normalized JSON schema
    llm_output = llm_router.generate(f"Parse this into JSON schema: {raw_input}", tier="cheap")
    
    # In a real system, we parse JSON strictly here
    try:
        normalized_data = {"vendor_name": "Acme Corp", "amount": 1250.0} # Simulated fallback
    except json.JSONDecodeError:
        normalized_data = {}
        
    # Log Audit
    state_manager.log_audit(
        thread_id=state.get("job_id", "unknown"),
        agent_node="InputAgent",
        action="Parsed raw input into normalized schema"
    )

    # Return the dictionary of state updates
    return {"normalized_data": normalized_data}
