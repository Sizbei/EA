import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from src.agents.travel_agent import TravelAgent
from src.agents.expense_agent import ExpenseAgent
from src.agents.calendar_agent import CalendarAgent

try:
    from composio import Composio
except ImportError:
    print("❌ Error: 'composio' package not found.")
    sys.exit(1)

# Mock classes for fallback
class MockOpenAI:
    def chat(self, *args, **kwargs):
        return self
    @property
    def completions(self): return self
    def create(self, *args, **kwargs):
        class Choice:
            def __init__(self): self.message = type('obj', (object,), {'content': "I'm a mock AI. Please set an API key to talk to a real model."})
        return type('obj', (object,), {'choices': [Choice()]})

def get_llm_client():
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
        sys.exit(1)

    try:
        # Composio 0.10.3 uses Composio() and string slugs
        toolset = Composio(api_key=api_key)
    except Exception as e:
        print(f"❌ Failed to initialize Composio: {e}")
        sys.exit(1)
    
    # Initialize Agents
    entity_id = os.getenv("USER_ENTITY_ID", "default")
    travel_agent = TravelAgent(client, toolset, entity_id)
    expense_agent = ExpenseAgent(client, toolset, entity_id)
    calendar_agent = CalendarAgent(client, toolset, entity_id)

    print("\ncommands: [setup] [monitor] [chat] [exit]")
    
    while True:
        user_input = input("> ").strip().lower()
        
        if user_input == 'exit':
            break
            
        elif user_input == 'setup':
            print("\n--- Running Initial Setup ---")
            travel_agent.setup_trackers()
            expense_agent.setup_tracker()
            calendar_agent.setup_task_database()
            print("--- Setup Complete ---\n")
            
        elif user_input == 'monitor':
            print("\n--- Monitoring for Flight & Expense Emails ---")
            print(" (Type Ctrl+C to stop)")
            try:
                import time
                while True: time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopped monitoring.")

        elif user_input == 'chat':
            query = input("Ask anything: ")
            
            # Select model name based on provider
            model_name = "gpt-4o"
            if os.getenv("DEEPSEEK_API_KEY"):
                model_name = "deepseek-chat"
            elif os.getenv("KIMI_API_KEY"):
                model_name = "moonshot-v1-8k"
            
            # Fetch tools using new SDK
            # user_id is the first positional argument in ts.tools.get()
            tools = toolset.tools.get(entity_id, toolkits=['googlesuper', 'notion'])
            
            # Basic pass-through to LLM
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": query}],
                tools=tools
            )
            print(f"🤖: {response.choices[0].message.content}")

if __name__ == "__main__":
    main()
