import os
from dotenv import load_dotenv
from composio import Composio

def test_sync():
    load_dotenv()
    api_key = os.getenv("COMPOSIO_API_KEY")
    entity_id = os.getenv("USER_ENTITY_ID", "default")
    
    ts = Composio(api_key=api_key)
    
    print(f"--- Manual Sync Test for {entity_id} ---")
    
    # 1. Search for flight emails
    print("Searching for 'flight confirmation' in Gmail...")
    emails = ts.tools.execute(
        slug="GMAIL_FETCH_EMAILS",
        arguments={"q": "flight confirmation", "max_results": 2},
        user_id=entity_id,
        dangerously_skip_version_check=True
    )
    
    print(f"Action Result: {emails}")
    
    # 2. Try to list files in drive to verify google super
    print("\nVerifying Drive access...")
    files = ts.tools.execute(
        slug="GOOGLESUPER_FIND_FILE",
        arguments={"q": "Flight Tracker"},
        user_id=entity_id,
        dangerously_skip_version_check=True
    )
    print(f"Drive Result: {files}")
    
    print("\n--- Sync Test Complete ---")

if __name__ == "__main__":
    test_sync()
