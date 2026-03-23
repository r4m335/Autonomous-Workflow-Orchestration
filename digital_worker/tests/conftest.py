import pytest
import os
import sqlite3
import tempfile
import shutil
from pathlib import Path

# Fix python path for tests if needed
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def temp_db():
    """Provides a temporary SQLite database for testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    yield path
    os.close(fd)
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def mock_workflow_state():
    """Standard initial state for workflow tests."""
    return {
        "job_id": "test-job-uuid",
        "tenant_id": "test-tenant",
        "is_dry_run": True,
        "raw_input": "Test input for workflow",
        "exceptions": [],
        "audit_trail": []
    }
