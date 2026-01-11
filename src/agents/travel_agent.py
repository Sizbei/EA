from composio import Composio

class TravelAgent:
    def __init__(self, client, toolset: Composio, entity_id: str = "default"):
        self.client = client
        self.toolset = toolset
        self.entity_id = entity_id
        self.flight_sheet_id = None
        self.housing_sheet_id = None

    def process_flight_email(self, email_content: str):
        """
        Parses flight info from email, saves to sheet, and adds to calendar.
        """
        print("Parsing flight email...")
        # (AI Logic would go here to extract specifics)
        # Placeholder data
        flight_data = {
            "flight_number": "UA123",
            "airline": "United",
            "departure_time": "2026-05-20T10:00:00Z",
            "arrival_time": "2026-05-20T13:00:00Z",
        }
        
        # 2. Add to Calendar
        self.toolset.tools.execute(
            slug="GOOGLESUPER_CREATE_EVENT",
            arguments={
                "summary": f"Flight {flight_data['flight_number']} ({flight_data['airline']})",
                "start": {"dateTime": flight_data['departure_time']},
                "end": {"dateTime": flight_data['arrival_time']},
                "description": f"Flight confirmation processed from email.\n\n{email_content[:200]}..."
            },
            user_id=self.entity_id,
            dangerously_skip_version_check=True
        )
        
        # 3. Add to Sheet
        if self.flight_sheet_id:
            self.toolset.tools.execute(
                slug="GOOGLESUPER_CREATE_SPREADSHEET_ROW",
                arguments={
                    "spreadsheetId": self.flight_sheet_id,
                    "values": [
                        "2026-05-01", 
                        flight_data['flight_number'], 
                        flight_data['airline'], 
                        "SFO", "JFK", "Confirmed"
                    ]
                },
                user_id=self.entity_id,
                dangerously_skip_version_check=True
            )
        
        print("✅ Flight processed successfully.")

    def setup_trackers(self):
        """
        Initializes the flight and housing trackers.
        """
        from src.utils.spreadsheet import SpreadsheetManager
        manager = SpreadsheetManager(self.toolset, self.entity_id)
        
        self.flight_sheet_id = manager.create_tracker_sheet(
            "Flight Tracker 2026",
            ["Date", "Flight Number", "Airline", "Departure", "Arrival", "Status"]
        )
        
        self.housing_sheet_id = manager.create_tracker_sheet(
            "Accommodation Tracker 2026",
            ["Date", "Property Name", "Address", "Check-in", "Check-out", "Confirmation #"]
        )
