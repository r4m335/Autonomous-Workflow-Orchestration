class EmailConnector:
    """
    Prebuilt connector for Email ingestion.
    Provides methods to pull IMAP/Gmail API data into the 
    raw_input text for the InputAgent.
    """
    def pull_unread_emails(self, inbox: str):
        # Simulate connecting to Office365 or Gmail
        print(f"[EmailConnector] Pulling unread emails for {inbox}")
        return [
            "FWD: Acme Corp Invoice #90210. Total $5400. Please process.",
            "Customer Support: My account is locked, I need assistance."
        ]

class CRMConnector:
    """
    Prebuilt connector for Salesforce / HubSpot API interaction.
    Fallback for execution_agent if Playwright is not needed.
    """
    def update_record(self, record_id: str, payload: dict):
        print(f"[CRMConnector] Pushing {payload} to Record {record_id}")
        return {"status": "200 OK"}
