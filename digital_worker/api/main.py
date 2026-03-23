from fastapi import FastAPI, BackgroundTasks, HTTPException, APIRouter
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, Optional
import sqlite3
import json
import os
import sys

# Ensure we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db
from core.orchestrator import Orchestrator
from api.dashboard import router as dashboard_router

app = FastAPI(title="Adaptive Digital Worker Platform")

# Mount Static Files for the Frontend
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Register the dashboard and observability router
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "Digital Worker Platform is online. Use /dashboard/execute to trigger DAG."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
