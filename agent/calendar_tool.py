import os
import stat
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def _get_paths():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return (
        os.environ.get("CREDENTIALS_FILE", os.path.join(base, "credentials.json")),
        os.environ.get("TOKEN_FILE", os.path.join(base, "token.json"))
    )

def get_calendar_service():
    credentials_file, token_file = _get_paths()
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        fd = os.open(token_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

def get_todays_events():
    service = get_calendar_service()
    local_now = datetime.now()
    today = local_now.date()
    time_min = datetime(today.year, today.month, today.day, 0, 0, 0,
                        tzinfo=timezone.utc).isoformat()
    time_max = datetime(today.year, today.month, today.day, 23, 59, 59,
                        tzinfo=timezone.utc).isoformat()

    calendars = service.calendarList().list().execute()
    all_events = []
    for cal in calendars.get("items", []):
        result = service.events().list(
            calendarId=cal["id"],
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