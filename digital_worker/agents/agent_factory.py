from typing import Dict, Any

def execute_agent(step_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Factory that routes to the correct agent based on 'agent_type'.
    """
    agent_type = step_config.get("agent_type")
    
    if agent_type == "extraction":
        from agents.extraction_agent import run_extraction
        return run_extraction(step_config, context)
        
    elif agent_type == "browser":
        from agents.browser_agent import run_browser
        return run_browser(step_config, context)
        
    elif agent_type == "reporting":
        from agents.reporting_agent import run_reporting
        return run_reporting(step_config, context)
        
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")
