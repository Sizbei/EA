from composio import Composio, Action
import os

def setup_triggers(travel_agent, expense_agent):
    """
    Sets up Gmail triggers to route emails to appropriate agents.
    """
    composio_client = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))
    
    # 1. Flight Confirmation Trigger
    # Listens for emails from major airlines with specific keywords
    flight_trigger = composio_client.triggers.create(
        name="Flight Monitor",
        trigger_name="GMAIL_NEW_EMAIL_RECEIVED",
        config={
            "query": "from:(delta.com OR united.com OR aa.com) subject:(confirmation OR itinerary)",
            "labelIds": ["INBOX"]
        }
    )
    
    # 2. Expense Trigger
    # Listens for receipts or invoices
    expense_trigger = composio_client.triggers.create(
        name="Expense Monitor",
        trigger_name="GMAIL_NEW_EMAIL_RECEIVED",
        config={
            "query": "has:attachment (receipt OR invoice) OR subject:(receipt OR invoice)",
            "labelIds": ["INBOX"]
        }
    )
    
    print("✅ Triggers configured for Flights and Expenses.")
    
    # Subscription loop would go here in a real deployment
    # subscribe_to_triggers(flight_trigger, expense_trigger, ...)
