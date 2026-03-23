from fastapi import APIRouter, HTTPException
from core.dag_engine import dag_app
from core.state_manager import state_manager
from core.config import settings
from core.logger import logger
import uuid

router = APIRouter(prefix="/dashboard")

@router.post("/execute")
async def execute_dag(raw_input: str, is_dry_run: bool = False, tenant_id: str = None):
    thread_id = str(uuid.uuid4())
    tenant = tenant_id or settings.default_tenant
    
    logger.info("Executing Dashboard Workflow Trigger", thread_id=thread_id, tenant=tenant)
    
    initial_input = {
        "job_id": thread_id,
        "tenant_id": tenant,
        "is_dry_run": is_dry_run,
        "raw_input": raw_input,
        "exceptions": [],
        "audit_trail": []
    }
    
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Internal start
        dag_app.invoke(initial_input, config)
        return {"thread_id": thread_id, "status": "initiated"}
    except Exception as e:
        logger.error(f"DAG Execution Failed: {str(e)}", thread_id=thread_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{thread_id}")
async def get_status(thread_id: str):
    try:
        state_config = {"configurable": {"thread_id": thread_id}}
        current_state = dag_app.get_state(state_config)
        
        vals = current_state.values if current_state and current_state.values else {}
        return {"status": "success", "state": vals}
    except Exception as e:
        logger.warning(f"Failed to fetch state for thread {thread_id}", thread_id=thread_id)
        raise HTTPException(status_code=404, detail="Thread not found")
