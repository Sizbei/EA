from composio import ComposioToolSet, Action
from src.utils.spreadsheet import SpreadsheetManager

class ExpenseAgent:
    def __init__(self, client, toolset: ComposioToolSet):
        self.client = client
        self.toolset = toolset
        self.expense_sheet_id = None

    def setup_tracker(self):
        """
        Creates the Expense Tracker sheet.
        """
        manager = SpreadsheetManager(self.toolset)
        self.expense_sheet_id = manager.create_tracker_sheet(
            "Expense Tracker 2026",
            ["Date", "Vendor", "Description", "Amount", "Category", "Receipt Link", "Status"]
        )

    def process_expense_email(self, email_data):
        """
        Extracts receipt info and updates sheet.
        """
        print("💰 Processing expense email...")
        # Mock extraction
        expense_info = {
            "date": "2026-05-20",
            "vendor": "Uber",
            "amount": "25.50",
            "category": "Ground Transport"
        }
        
        # Add to sheet logic would go here
        print(f"Logged expense: {expense_info['vendor']} - ${expense_info['amount']}")
