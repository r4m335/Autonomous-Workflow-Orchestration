from fastapi import FastAPI, APIRouter, HTTPException
from core.dag_engine import dag_app
from core.state_manager import state_manager
import uuid

# Fast API Router for Control Panel & Observability
router = APIRouter(prefix="/dashboard", tags=["observability"])

@router.get("/status/{thread_id}")
def get_workflow_status(thread_id: str):
    """Real-time workflow visualization and state fetch."""
    try:
        # Fetch the LangGraph checkpoint state
        state_config = {"configurable": {"thread_id": thread_id}}
        current_state = dag_app.get_state(state_config)
        
        # Ensure audit_trail exists
        vals = current_state.values if current_state and current_state.values else {}
        return {"status": "success", "state": vals}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"State fetch failed: {str(e)}")

@router.post("/replay/{thread_id}")
def replay_workflow(thread_id: str):
    """
    Replay system: Re-runs the exact workflow with the same inputs.
    We retrieve the inputs from the checkpointer and stream a new thread.
    """
    old_state_config = {"configurable": {"thread_id": thread_id}}
    old_state = dag_app.get_state(old_state_config)
    
    if not old_state or not old_state.values:
        raise HTTPException(status_code=404, detail="Original thread not found for replay")
        
    new_thread_id = f"replay_{uuid.uuid4()}"
    new_state_config = {"configurable": {"thread_id": new_thread_id}}
    
    # We pass the raw_input into the DAG to trigger replay
    initial_input = {"raw_input": old_state.values.get("raw_input", ""), "job_id": new_thread_id, "is_dry_run": False}
    
    result = list(dag_app.stream(initial_input, new_state_config))
    return {"message": "Replay started", "new_thread_id": new_thread_id, "stream_output": result}

@router.post("/execute")
def execute_workflow(raw_input: str, is_dry_run: bool = False, tenant_id: str = "tenant_a"):
    """Entrypoint triggered by integrations to start the DAG."""
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "job_id": thread_id,
        "tenant_id": tenant_id,
        "is_dry_run": is_dry_run,
        "raw_input": raw_input,
        "exceptions": [],
        "audit_trail": []
    }
    
    # Streams execution through the DAG (in production, we queue this via celery/Redis)
    events = list(dag_app.stream(initial_state, config))
    
    # Return the final resulting state
    final_state = dag_app.get_state(config)
    return {"thread_id": thread_id, "final_state": final_state.values}
