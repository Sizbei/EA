import os
import sys
from dotenv import load_dotenv
from composio import Composio
from src.utils.inbox_cleaner import InboxCleaner

def main():
    load_dotenv()
    api_key = os.getenv("COMPOSIO_API_KEY")
    entity_id = os.getenv("USER_ENTITY_ID", "default")
    
    if not api_key:
        print("❌ COMPOSIO_API_KEY not found.")
        return

    ts = Composio(api_key=api_key)
    cleaner = InboxCleaner(ts, entity_id)
    
    print("--- 📧 Inbox Cleanup Assistant ---")
    
    # Run a basic scan
    cleaner.list_potential_bloat()
    
    print("\nSuggestions:")
    print("1. Archive all unread promotions (is:unread category:promotions)")
    print("2. Archive all unread social updates (is:unread category:social)")
    print("3. Custom Cleanup (enter query)")
    
    # Note: In a real interactive session, we'd wait for input.
    # For now, I'll just finish the scan.

if __name__ == "__main__":
    main()
