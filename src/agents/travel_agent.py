from composio import ComposioToolSet, Action
# from openai import OpenAI # injected in main

class TravelAgent:
    def __init__(self, client, toolset: ComposioToolSet):
        self.client = client
        self.toolset = toolset
        self.flight_sheet_id = None
        self.housing_sheet_id = None

    def process_flight_confirmation(self, email_content: str):
        """
        Analyzes email content, extracts flight info, and updates Calendar + Sheets.
        """
        print("✈️ Processing flight confirmation...")
        
        # 1. Extract Details (Mocking LLM extraction for now)
        # In real scenario: ask LLM to parse JSON
        flight_data = {
            "flight_number": "DL123", # Mock
            "departure_time": "2026-05-20T10:00:00",
            "arrival_time": "2026-05-20T14:00:00", 
            "airline": "Delta"
        }
        
        # 2. Add to Calendar
        self.toolset.execute_action(
            Action.GOOGLECALENDAR_CREATE_EVENT,
            params={
                "summary": f"Flight {flight_data['flight_number']} ({flight_data['airline']})",
                "start": {"dateTime": flight_data['departure_time']},
                "end": {"dateTime": flight_data['arrival_time']},
                "description": f"Flight confirmation processed from email.\n\n{email_content[:200]}..."
            }
        )
        
        # 3. Add to Sheet
        # if self.flight_sheet_id:
        #     add_row(self.flight_sheet_id, flight_data)
            
        return "Flight processed successfully."

    def setup_trackers(self):
        """
        Initializes the flight and housing trackers.
        """
        from src.utils.spreadsheet import SpreadsheetManager
        manager = SpreadsheetManager(self.toolset)
        
        self.flight_sheet_id = manager.create_tracker_sheet(
            "Flight Tracker 2026",
            ["Date", "Flight Number", "Airline", "Departure", "Arrival", "Status"]
        )
        
        self.housing_sheet_id = manager.create_tracker_sheet(
            "Accommodation Tracker 2026",
            ["Check-in", "Check-out", "Property", "Address", "Conf #", "Cost"]
        )
