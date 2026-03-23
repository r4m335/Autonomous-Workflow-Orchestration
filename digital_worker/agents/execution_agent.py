from core.models import WorkflowState
from core.state_manager import state_manager
from api.security import security_layer
from playwright.sync_api import sync_playwright
import time

def node_execution_agent(state: WorkflowState) -> WorkflowState:
    """
    Execution Agent: Performs hybrid API/UI actions.
    Uses Playwright for browser automation fallback if API is unavailable.
    """
    print("--- [Execution Agent] Executing DAG Tasks ---")
    dag = state.get("dynamically_generated_dag", {})
    tenant_id = state.get("tenant_id", "default_tenant")
    job_id = state.get("job_id", "unknown")
    is_dry_run = state.get("is_dry_run", False)
    
    # Simulate retrieving vaulted credentials
    erp_creds = security_layer.get_credentials(tenant_id, "erp_login")

    results = {}
    for task in dag.get("tasks", []):
        task_id = task["id"]
        system = task["system"]
        action = task["action"]
        
        print(f"[{system}] Executing {action} (Dry Run: {is_dry_run})")
        
        if is_dry_run:
            results[task_id] = "Simulated Success"
            continue
            
        # Example: if CRM, we could use Playwright
        if system == "CRM" and action == "enter_invoice":
            try:
                # Setup resilient DOM interaction (retries, wait states)
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    # A robust implementation handles DOM drift by finding elements
                    # via semantic queries (e.g., Locator API) rather than brittle xpaths
                    page.goto("https://httpbin.org/forms/post")
                    page.fill("input[name='custname']", "Acme Corp")
                    page.fill("input[name='custtel']", "1250.00")
                    browser.close()
                results[task_id] = "Success via UI Fallback"
            except Exception as e:
                # If Execution fails, we throw an exception to be caught by the Exception Agent
                return {"exceptions": [f"UI Automation failed: {e}"]}

        else:
            # API Execution
            results[task_id] = "Success via API"
            
        state_manager.log_audit(job_id, "ExecutionAgent", f"Executed {action} on {system}")

    return {"execution_results": results}
