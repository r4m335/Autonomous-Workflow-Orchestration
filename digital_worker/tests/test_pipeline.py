import pytest
import uuid
import time
from core.dag_engine import dag_app

@pytest.mark.asyncio
async def test_full_pipeline_e2e():
    """Verifies the complete pipeline from ingestion to final validation."""
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_input = {
        "job_id": thread_id,
        "tenant_id": "tenant_a",
        "is_dry_run": True,
        "raw_input": "Please process the invoice for Acme Corp. Total is $1250.",
        "exceptions": [],
        "audit_trail": []
    }
    
    # Execute the workflow
    result = dag_app.invoke(initial_input, config)
    
    # Assertions
    assert "normalized_data" in result
    assert result["normalized_data"]["vendor_name"] == "Acme Corp"
    assert "validation_score" in result
    assert result["validation_score"] >= 0.8 # Target for successful extraction
    
    # Check audit trail
    assert len(result.get("audit_trail", [])) > 0
