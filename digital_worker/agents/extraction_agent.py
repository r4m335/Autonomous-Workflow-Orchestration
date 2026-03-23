import json
import re
from typing import Dict, Any

def run_extraction(step_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates extracting data from an unstructured source (e.g. PDF).
    In a real scenario, this would call an LLM (Ollama or OpenAI API) 
    and pass in the text/images to extract the 'expected_fields'.
    """
    config = step_config.get("config", {})
    expected_fields = config.get("expected_fields", [])
    
    print(f"[Extraction Agent] Extracting fields: {expected_fields}")
    
    # We will look at context to see if there's raw_text or a file_path
    raw_text = context.get("raw_text", "")
    
    # Simple mock that fakes an LLM response if the text is empty
    if not raw_text:
        print("[Extraction Agent] No raw_text provided. Generating simulated dummy invoice extraction...")
        # Simulating LLM JSON response
        return {
            "vendor_name": "Acme Corp",
            "total_amount": "1250.00",
            "invoice_date": "2026-03-23"
        }
        
    # If there is raw text, we simulate an LLM parsing it using regex (dummy implementation)
    # A real implementation would cast an HTTP POST to an LLM provider:
    # prompt = f"Extract {expected_fields} from the following text as JSON: \n\n{raw_text}"
    # response = requests.post(...)
    
    result = {}
    for field in expected_fields:
        result[field] = "Extracted_Value_Placeholder"
    
    return result
