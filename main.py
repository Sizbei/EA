import os
import sys
from dotenv import load_dotenv
from src.agents.travel_agent import TravelAgent
from src.agents.expense_agent import ExpenseAgent
from src.agents.calendar_agent import CalendarAgent

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from composio import ComposioToolSet, App
except ImportError:
    print("Composio SDK not found. Install with `pip install composio-core`")
    sys.exit(1)

# Mock OpenAI for now since user has no key
class MockOpenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.chat = self.Chat()

    class Chat:
        def __init__(self):
            self.completions = self.Completions()

        class Completions:
            def create(self, model, messages, tools=None):
                print(f"\n[MockLLM] Processing request: {messages[-1]['content']}")
                # Simple heuristic response for testing
                return self.MockResponse()

            class MockResponse:
                class Choice:
                    class Message:
                        content = "I'm a mock assistant. I haven't implemented logic yet, but I received your request!"
                        tool_calls = None
                    finish_reason = "stop"
                    message = Message()
                
                choices = [Choice()]

# Try importing real OpenAI, else fallback
try:
    from openai import OpenAI
except ImportError:
    OpenAI = MockOpenAI

load_dotenv()

def get_llm_client():
    """Initializes the LLM client based on available environment variables."""
    # DeepSeek (Recommended for free tier)
    if os.getenv("DEEPSEEK_API_KEY"):
        print("🚀 Using DeepSeek Engine")
        return OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
    # Moonshot / Kimi
    elif os.getenv("KIMI_API_KEY"):
        print("🌙 Using Kimi (Moonshot) Engine")
        return OpenAI(
            api_key=os.getenv("KIMI_API_KEY"),
            base_url="https://api.moonshot.ai/v1"
        )
    # OpenAI (Standard)
    elif os.getenv("OPENAI_API_KEY"):
        print("🤖 Using OpenAI Engine")
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("⚠️  No API Key found. Using Mock LLM.")
    return MockOpenAI()

def main():
    print("🤖 Composio Executive Assistant Starting...")
    load_dotenv()
    
    client = get_llm_client()

    # Initialize Composio
    api_key = os.getenv("COMPOSIO_API_KEY")
    if not api_key:
        print("❌ Error: COMPOSIO_API_KEY is not set.")
        print("Please run 'export COMPOSIO_API_KEY=your_key' or set it in .env")
        print("You can find your key at https://app.composio.dev")
        sys.exit(1)

    try:
        toolset = ComposioToolSet()
    except Exception as e:
        print(f"❌ Failed to initialize Composio: {e}")
        sys.exit(1)
    
    # Initialize Agents
    travel_agent = TravelAgent(client, toolset)
    expense_agent = ExpenseAgent(client, toolset)
    calendar_agent = CalendarAgent(client, toolset)

    print("\ncommands: [setup] [monitor] [chat] [exit]")
    
    while True:
        user_input = input("\n> ").strip().lower()
        
        if user_input == 'exit':
            break
            
        elif user_input == 'setup':
            print("\n--- Running Initial Setup ---")
            travel_agent.setup_trackers()
            expense_agent.setup_tracker()
            calendar_agent.setup_task_database()
            print("--- Setup Complete ---\n")
            
        elif user_input == 'monitor':
            print("\n--- Starting Triggers ---")
            from src.triggers.email_monitors import setup_triggers
            setup_triggers(travel_agent, expense_agent)
            print("(Note: In a real app, this would block/listen eternally)")
            
        elif user_input == 'chat':
            query = input("Ask anything: ")
            
            # Select model name based on provider
            model_name = "gpt-4o" # Default
            if os.getenv("DEEPSEEK_API_KEY"):
                model_name = "deepseek-chat"
            elif os.getenv("KIMI_API_KEY"):
                model_name = "moonshot-v1-8k"
            
            # Basic pass-through to LLM
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": query}],
                tools=toolset.get_tools(apps=[App.GMAIL, App.GOOGLECALENDAR])
            )
            print(f"🤖: {response.choices[0].message.content}")
            
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
