from composio import ComposioToolSet, Action

class SpreadsheetManager:
    def __init__(self, toolset: ComposioToolSet):
        self.toolset = toolset

    def create_tracker_sheet(self, title: str, columns: list):
        """
        Creates a new Google Sheet with the given title and header columns.
        Returns the spreadsheet ID.
        """
        print(f"Creating spreadsheet: {title}")
        
        # 1. Create Sheet
        result = self.toolset.execute_action(
            Action.GOOGLESHEETS_CREATE_GOOGLE_SHEET1,
            params={"properties": {"title": title}}
        )
        print(f"DEBUG: result={result}")
        # Note: Actual return structure depends on API, mocking simplified access
        spreadsheet_id = result.get('spreadsheetId')
        
        if not spreadsheet_id:
            print("Failed to create spreadsheet.")
            return None

        # 2. Add Headers
        # Construct range 'A1:Z1' roughly
        self.toolset.execute_action(
            Action.GOOGLESHEETS_BATCH_UPDATE,
            params={
                "spreadsheetId": spreadsheet_id,
                "values": [columns],
                "range": "Sheet1!A1"
            }
        )
        
        print(f"✅ Created '{title}' (ID: {spreadsheet_id})")
        return spreadsheet_id
