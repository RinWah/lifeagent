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
    now = datetime.now(timezone.utc).isoformat()
    today_end = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59).isoformat()
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        timeMax=today_end,
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    return events_result.get("items", [])

if __name__ == "__main__":
    events = get_todays_events()
    if not events:
        print("No events today.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"{start}: {event.get('summary', 'No title')}")