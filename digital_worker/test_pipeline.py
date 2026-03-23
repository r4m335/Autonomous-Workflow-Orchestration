import os
import sys
import json
import time

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.db import get_db, init_db
from core.orchestrator import Orchestrator

def test_run():
    init_db()
    orc = Orchestrator()
    
    # 1. Start Job
    print("--- Starting Job ---")
    initial_context = {
        "raw_text": "Invoice #12345 from Acme Corp. Total: 1250.00 Date: 2026-03-23"
    }
    job_id = orc.start_job("invoice_processing", initial_context)
    print(f"Job ID: {job_id}")
    
    # 2. Run steps until complete
    while True:
        result = orc.run_step(job_id)
        status = result.get("status")
        print(f"Step Result: {result}")
        if status in ["COMPLETED", "FAILED"]:
            break
        time.sleep(1) # small pause
        
    # 3. Verify DB State
    conn = get_db()
    cursor = conn.cursor()
    job = cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
    print("\n--- Final Job State ---")
    print(f"Status: {job['status']}")
    print(f"Context: {json.loads(job['context'])}")
    
    steps = cursor.execute("SELECT * FROM steps WHERE job_id = ?", (job_id,)).fetchall()
    print("\n--- Steps Executed ---")
    for s in steps:
        print(f"[{s['id']}] {s['step_name']} ({s['agent_type']}) - {s['status']}")
        
    audit = cursor.execute("SELECT * FROM audit_logs WHERE job_id = ?", (job_id,)).fetchall()
    print("\n--- Audit Logs ---")
    for a in audit:
        print(f"{a['timestamp']} - {a['action']}: {a['details']}")

if __name__ == "__main__":
    test_run()
