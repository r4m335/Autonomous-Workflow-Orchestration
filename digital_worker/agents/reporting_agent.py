from typing import Dict, Any

def run_reporting(step_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a final report or notification based on the context data.
    """
    config = step_config.get("config", {})
    message_template = config.get("message_template", "Job completed.")
    
    # Format the message using Python string formatting, pulling from context
    try:
        final_message = message_template.format(**context)
    except KeyError as e:
        final_message = f"Job completed, but missing formatting key: {e}"
        
    print("="*40)
    print(f"[Reporting Agent] NOTIFICATION DISPATCHED")
    print(f"Message: {final_message}")
    print("="*40)
    
    # In a real environment, this might call SendGrid, Slack API, or MS Teams Webhook.
    
    return {"notification_sent": True, "final_message": final_message}
