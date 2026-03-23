from fastapi import FastAPI, BackgroundTasks, HTTPException, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import sys

# Ensure we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings
from core.logger import logger
from api.dashboard import router as dashboard_router
from api.custom_docs import get_premium_swagger_ui_html

app = FastAPI(
    title=settings.app_name,
    docs_url=None, # Disable default
    redoc_url=None
)

# Custom Premium Docs Endpoint
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_premium_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Premium API Docs"
    )

# Mount Static Files for the Frontend
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Register the dashboard and observability router
app.include_router(dashboard_router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": f"{settings.app_name} is online. Use /dashboard/execute to trigger DAG."}

def main():
    import uvicorn
    logger.info(f"Starting {settings.app_name} server...")
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=settings.debug)

if __name__ == "__main__":
    main()
