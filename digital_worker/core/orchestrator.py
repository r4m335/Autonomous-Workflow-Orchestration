import json
import os
import uuid
import sys
from typing import Dict, Any

# Ensure we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db, create_job, log_audit

WORKFLOWS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "workflows")

class Orchestrator:
    def __init__(self):
        pass

    def load_workflow(self, name: str) -> Dict[str, Any]:
        path = os.path.join(WORKFLOWS_DIR, f"{name}.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Workflow {name} not found.")
        with open(path, "r") as f:
            return json.load(f)

    def start_job(self, workflow_name: str, initial_data: Dict[str, Any]) -> str:
        workflow = self.load_workflow(workflow_name)
        job_id = str(uuid.uuid4())
        
        # Initialize job in DB
        create_job(job_id, workflow_name, initial_context=initial_data)
        log_audit(job_id, "JOB_STARTED", f"Started workflow {workflow_name}")
        
        # We start the first step asynchronously or synchronously based on the setup.
        # For this orchestrator, we'll provide a method to drive the workflow step-by-step
        return job_id

    def run_step(self, job_id: str):
        """
        Executes the current pending step for a given job.
        In a full system, this would be picked up by a celery/backgroud worker.
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # Get Job status
        job_row = cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        if not job_row:
            raise ValueError("Job not found")
        if job_row["status"] != "PENDING" and job_row["status"] != "RUNNING":
            return {"status": job_row["status"], "message": "Job is no longer active."}

        # Find the next step to execute based on context or workflow def.
        # For simplicity, if we don't have any completed steps in DB, it's the first step.
        workflow = self.load_workflow(job_row["workflow_name"])
        
        # Find last completed step
        last_step_row = cursor.execute(
            "SELECT * FROM steps WHERE job_id = ? ORDER BY id DESC LIMIT 1", (job_id,)
        ).fetchone()

        context = json.loads(job_row["context"])
        
        step_to_run = None
        if not last_step_row:
            # First step
            step_to_run = workflow["steps"][0]
        else:
            if last_step_row["status"] == "COMPLETED":
                # Find the next step based on the workflow definition
                # We need to map step_name -> step
                step_def = next((s for s in workflow["steps"] if s["step_name"] == last_step_row["step_name"]), None)
                next_step_name = step_def.get("next") if step_def else None
                if not next_step_name:
                    # Workflow is complete
                    cursor.execute("UPDATE jobs SET status = 'COMPLETED' WHERE job_id = ?", (job_id,))
                    conn.commit()
                    log_audit(job_id, "JOB_COMPLETED")
                    return {"status": "COMPLETED", "message": "Workflow completed successfully."}
                
                step_to_run = next((s for s in workflow["steps"] if s["step_name"] == next_step_name), None)
            else:
                return {"status": last_step_row["status"], "message": f"Step {last_step_row['step_name']} is {last_step_row['status']}"}

        if not step_to_run:
            raise ValueError("Next step not found in workflow definition.")

        # Log new step creation
        cursor.execute(
            """INSERT INTO steps (job_id, step_name, agent_type, status, input_data) 
               VALUES (?, ?, ?, ?, ?)""",
            (job_id, step_to_run["step_name"], step_to_run["agent_type"], "PENDING", json.dumps(context))
        )
        step_id = cursor.lastrowid
        cursor.execute("UPDATE jobs SET status = 'RUNNING' WHERE job_id = ?", (job_id,))
        conn.commit()
        log_audit(job_id, "STEP_STARTED", f"Starting '{step_to_run['step_name']}' via {step_to_run['agent_type']}", step_id)
        
        # Now Execute It
        from agents.agent_factory import execute_agent
        try:
            # We pass the full configuration of the block plus context
            result = execute_agent(step_to_run, context)
            
            # Update step success
            context.update(result) # Merge context
            cursor.execute(
                "UPDATE steps SET status = 'COMPLETED', output_data = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(result), step_id)
            )
            cursor.execute("UPDATE jobs SET context = ? WHERE job_id = ?", (json.dumps(context), job_id))
            conn.commit()
            log_audit(job_id, "STEP_COMPLETED", f"Step '{step_to_run['step_name']}' completed.", step_id)

            return {"status": "STEP_COMPLETED"}

        except Exception as e:
            cursor.execute(
                "UPDATE steps SET status = 'FAILED', error_message = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?",
                (str(e), step_id)
            )
            cursor.execute("UPDATE jobs SET status = 'FAILED' WHERE job_id = ?", (job_id,))
            conn.commit()
            log_audit(job_id, "STEP_FAILED", f"Error: {str(e)}", step_id)
            return {"status": "FAILED", "error": str(e)}
        finally:
            conn.close()

if __name__ == "__main__":
    from database.db import init_db
    init_db()
    orc = Orchestrator()
    print("Orchestrator ready.")
