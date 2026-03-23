from typing import Dict, Any
from playwright.sync_api import sync_playwright

def run_browser(step_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Uses Playwright to automate data entry based on the context payload.
    """
    config = step_config.get("config", {})
    url = config.get("url")
    form_mapping = config.get("form_mapping", {})
    
    print(f"[Browser Agent] Navigating to {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Headless=False for demo purposes
        page = browser.new_page()
        page.goto(url)
        
        # In a real scenario, the form_mapping dict maps CSS Selectors OR field names 
        # to the keys in our 'context'. 
        # For this demo, let's assume form_mapping maps input 'name' attributes to context keys.
        
        for input_name, context_key in form_mapping.items():
            value_to_enter = context.get(context_key, "")
            print(f"[Browser Agent] Entering '{value_to_enter}' into field '{input_name}'")
            
            # This is a very simplistic selector, standard CRM would be more complex
            selector = f"input[name='{input_name}']"
            
            try:
                page.fill(selector, str(value_to_enter))
            except Exception as e:
                print(f"[Browser Agent] Could not fill {selector}: {e}")
                # For demo fallback, if there's no such input field we just log it
        
        # Simulate form submit by clicking a button if defined, or just taking a screenshot
        page.screenshot(path="browser_agent_screenshot.png")
        print("[Browser Agent] Captured proof of entry.")
        
        browser.close()
        
    return {"browser_entry_status": "Success", "screenshot": "browser_agent_screenshot.png"}
