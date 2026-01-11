from composio import Composio

class SpreadsheetManager:
    def __init__(self, toolset: Composio, entity_id: str = "default"):
        self.toolset = toolset
        self.entity_id = entity_id

    def create_tracker_sheet(self, title: str, columns: list):
        """
        Creates a new Google Sheet with the given title and header columns.
        Returns the spreadsheet ID.
        """
        print(f"Creating spreadsheet: {title}")
        
        # 1. Create Sheet
        result = self.toolset.tools.execute(
            slug="GOOGLESUPER_CREATE_GOOGLE_SHEET1",
            arguments={"properties": {"title": title}},
            user_id=self.entity_id,
            dangerously_skip_version_check=True
        )
        
        # result is usually a dict or object with data
        # Let's check the structure in the execute response
        data = result if isinstance(result, dict) else (result.data if hasattr(result, 'data') else {})
        spreadsheet_id = data.get('spreadsheetId')
        
        if not spreadsheet_id:
            print(f"Failed to create spreadsheet. Result: {result}")
            return None

        # 2. Add Headers
        self.toolset.tools.execute(
            slug="GOOGLESUPER_BATCH_UPDATE",
            arguments={
                "spreadsheetId": spreadsheet_id,
                "values": [columns],
                "range": "Sheet1!A1"
            },
            user_id=self.entity_id,
            dangerously_skip_version_check=True
        )
        
        print(f"✅ Created '{title}' (ID: {spreadsheet_id})")
        return spreadsheet_id
