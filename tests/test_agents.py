import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.agents.travel_agent import TravelAgent
from src.agents.expense_agent import ExpenseAgent
from composio import Action

class TestAgents(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_toolset = MagicMock()
        
    def test_travel_agent_process_flight(self):
        agent = TravelAgent(self.mock_client, self.mock_toolset)
        
        # Mock email content
        email_content = "Flight confirmation for DL123 from JFK to LHR."
        
        # Run processing
        result = agent.process_flight_confirmation(email_content)
        
        # Verify tool called
        self.mock_toolset.execute_action.assert_called_with(
            Action.GOOGLECALENDAR_CREATE_EVENT,
            params={
                "summary": "Flight DL123 (Delta)",
                "start": {"dateTime": "2026-05-20T10:00:00"},
                "end": {"dateTime": "2026-05-20T14:00:00"},
                "description": unittest.mock.ANY
            }
        )
        self.assertEqual(result, "Flight processed successfully.")

    def test_expense_agent_setup(self):
        agent = ExpenseAgent(self.mock_client, self.mock_toolset)
        
        # Mock return for create_sheet
        # Note: SpreadsheetManager uses toolset.execute_action internally
        self.mock_toolset.execute_action.return_value = {"spreadsheetId": "mock_id_123"}
        
        agent.setup_tracker()
        
        # Verify calls
        # 1. Create Sheet
        self.mock_toolset.execute_action.assert_any_call(
            Action.GOOGLESHEETS_CREATE_SHEET,
            params={"title": "Expense Tracker 2026"}
        )
        # 2. Add Headers (Batch Update)
        self.mock_toolset.execute_action.assert_any_call(
            Action.GOOGLESHEETS_BATCH_UPDATE,
            params={
                "spreadsheetId": "mock_id_123",
                "values": [['Date', 'Vendor', 'Description', 'Amount', 'Category', 'Receipt Link', 'Status']],
                "range": "Sheet1!A1"
            }
        )
        self.assertEqual(agent.expense_sheet_id, "mock_id_123")

if __name__ == '__main__':
    unittest.main()
