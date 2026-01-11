import subprocess
import sys

REQUIRED_INTEGRATIONS = [
    "googlecalendar",
    "gmail",
    "googlesheets",
    "googledrive",
    "slack",
    "notion"
]

def check_composio_cli():
    """Check if composio CLI is installed."""
    try:
        subprocess.run(["composio", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 'composio' CLI not found. Please install it with 'pip install composio-core'.")
        return False

def check_integrations():
    """List active integrations (mocking/parsing CLI output)."""
    print("Checking installed integrations...")
    # This is a bit tricky to parse programmatically without the SDK being fully authenticated 
    # and having a way to list via SDK. For now, we'll just prompt the user.
    
    print("\nPlease ensure you have run 'composio login' first.\n")
    
    for integration in REQUIRED_INTEGRATIONS:
        print(f"👉 To install {integration}:  composio add {integration}")

def main():
    if not check_composio_cli():
        sys.exit(1)
        
    print("=== Composio Integration Setup ===")
    check_integrations()
    print("\n✅ Run the commands above in your terminal to authenticate these services.")

if __name__ == "__main__":
    main()
