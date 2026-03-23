from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

# State dictionary for LangGraph workflow
class WorkflowState(TypedDict):
    """
    Represents the state of the workflow passed between agents.
    Uses operator.add to append to lists (like logs/errors) when updating state.
    """
    tenant_id: str
    job_id: str
    
    # Dual-Execution mode
    is_dry_run: bool
    
    # System Context
    raw_input: str
    normalized_data: dict
    
    # Workflow intelligence
    intent: str
    dynamically_generated_dag: dict
    
    # Execution Tracking
    current_action: dict
    execution_results: dict
    validation_score: float
    
    # Logs and feedback
    audit_trail: Annotated[List[str], operator.add]
    exceptions: Annotated[List[str], operator.add]
