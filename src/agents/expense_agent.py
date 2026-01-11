from composio import Composio
from src.utils.spreadsheet import SpreadsheetManager

class ExpenseAgent:
    def __init__(self, client, toolset: Composio, entity_id: str = "default"):
        self.client = client
        self.toolset = toolset
        self.entity_id = entity_id
        self.expense_sheet_id = None

    def setup_tracker(self):
        """
        Creates the Expense Tracker sheet.
        """
        manager = SpreadsheetManager(self.toolset, self.entity_id)
        self.expense_sheet_id = manager.create_tracker_sheet(
            "Expense Tracker 2026",
            ["Date", "Vendor", "Description", "Amount", "Category", "Receipt Link", "Status"]
        )

    def log_expense(self, expense_data: dict):
        """
        Logs an expense to the sheet.
        """
        if not self.expense_sheet_id:
            print("Expense sheet not found.")
            return

        self.toolset.tools.execute(
            slug="GOOGLESUPER_CREATE_SPREADSHEET_ROW",
            arguments={
                "spreadsheetId": self.expense_sheet_id,
                "values": [
                    expense_data.get('date'),
                    expense_data.get('vendor'),
                    expense_data.get('description'),
                    expense_data.get('amount'),
                    expense_data.get('category'),
                    expense_data.get('receipt_link'),
                    "Logged"
                ]
            },
            user_id=self.entity_id,
            dangerously_skip_version_check=True
        )
        print(f"✅ Expense logged: {expense_data.get('vendor')} - ${expense_data.get('amount')}")
