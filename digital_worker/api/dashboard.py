from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from core.dag_engine import dag_app
from core.state_manager import state_manager
from core.config import settings
from core.logger import logger
import uuid
from typing import Optional

router = APIRouter(prefix="/dashboard")

class ExecuteRequest(BaseModel):
    raw_input: str = Field(..., description="The messy BPO input to process")
    is_dry_run: bool = Field(False, description="Whether to commit changes or just simulate")
    tenant_id: Optional[str] = Field(None, description="The tenant context for the worker")

def run_workflow_background(thread_id: str, initial_input: dict, config: dict):
    """Background task to execute the LangGraph workflow."""
    try:
        logger.info("Starting background workflow execution", thread_id=thread_id)
        dag_app.invoke(initial_input, config)
        logger.info("Background workflow execution completed", thread_id=thread_id)
    except Exception as e:
        logger.error(f"Background Workflow Error: {str(e)}", thread_id=thread_id)

@router.post("/execute")
async def execute_dag(request: ExecuteRequest, background_tasks: BackgroundTasks):
    thread_id = str(uuid.uuid4())
    tenant = request.tenant_id or settings.default_tenant
    
    logger.info("Received Workflow Trigger", thread_id=thread_id, tenant=tenant)
    
    initial_input = {
        "job_id": thread_id,
        "tenant_id": tenant,
        "is_dry_run": request.is_dry_run,
        "raw_input": request.raw_input,
        "exceptions": [],
        "audit_trail": []
    }
    
    config = {"configurable": {"thread_id": thread_id}}
    
    # Add to background tasks to prevent API timeout
    background_tasks.add_task(run_workflow_background, thread_id, initial_input, config)
    
    return {
        "thread_id": thread_id, 
        "status": "accepted",
        "message": "Workflow started in background"
    }

@router.get("/status/{thread_id}")
async def get_status(thread_id: str):
    try:
        state_config = {"configurable": {"thread_id": thread_id}}
        current_state = dag_app.get_state(state_config)
        
        # If state doesn't exist yet, it's still initializing
        if not current_state or not current_state.values:
             return {"status": "processing", "thread_id": thread_id}
             
        return {"status": "success", "state": current_state.values}
    except Exception as e:
        logger.warning(f"Thread lookup failed for {thread_id}", thread_id=thread_id)
        raise HTTPException(status_code=404, detail="Thread not found")
