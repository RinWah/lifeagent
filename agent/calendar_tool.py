import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = os.path.expanduser("~/lifeagent/credentials.json")
TOKEN_FILE = os.path.expanduser("~/lifeagent/token.json")

def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def get_todays_events():
    service = get_calendar_service()
    today = datetime.now(timezone.utc).date()
    time_min = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=timezone.utc).isoformat()
    time_max = datetime(today.year, today.month, today.day, 23, 59, 59, tzinfo=timezone.utc).isoformat()
    
    calendars = service.calendarList().list().execute()
    all_events = []
    
    for cal in calendars.get("items", []):
        cal_id = cal["id"]
        result = service.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        all_events.extend(result.get("items", []))
    
    return all_events

if __name__ == "__main__":
    events = get_todays_events()
    if not events:
        print("No events today.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"{start}: {event.get('summary', 'No title')}")