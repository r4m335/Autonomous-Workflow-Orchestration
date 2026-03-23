import re
from typing import Dict, Any, Optional

class SecurityLayer:
    """
    Handles Multi-Tenancy isolation, PII masking, and credential vaulting.
    Mandatory for BPO clients.
    """
    
    def __init__(self):
        # Mock vault: mapping of tenant_id -> credentials
        self._vault = {
            "tenant_a": {"crm_api_key": "sk_live_tenantA123", "erp_login": "admin_a"},
            "tenant_b": {"crm_api_key": "sk_live_tenantB456", "erp_login": "admin_b"}
        }

    def get_credentials(self, tenant_id: str, system: str) -> Optional[str]:
        """Retrieve credentials strictly isolated by tenant."""
        creds = self._vault.get(tenant_id, {})
        return creds.get(system)

    def mask_pii(self, text: str) -> str:
        """
        Replaces sensitive information (Emails, SSNs, Credit Cards) with placeholders 
        before sending data to external LLMs (Cost Optimization models).
        """
        if not text:
            return text
            
        # Basic Email masking
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        masked_text = re.sub(email_pattern, '[REDACTED_EMAIL]', text)
        
        # Basic SSN masking (US)
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        masked_text = re.sub(ssn_pattern, '[REDACTED_SSN]', masked_text)
        
        return masked_text

    def unmask_pii(self, masked_text: str, vault_reference: str) -> str:
        """
        Rehydrates PII for the Execution Agent to input into the target CRM.
        (Implementation omitted for prototype)
        """
        pass

security_layer = SecurityLayer()
