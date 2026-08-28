import os
import time
from datetime import datetime
from ntfy import notify
from calendar_tool import get_todays_events

# --- Routine config ---
ROUTINES = {
    "meds": {"time": "08:00", "message": "Time to take your meds! 💊", "title": "Meds Reminder"},
    "sleep": {"time": "23:00", "message": "Bedtime soon — start winding down 🌙", "title": "Sleep Reminder"},
    "laundry": {"duration_minutes": 45, "message": "Laundry's done! 🧺", "title": "Laundry Done"},
}

def check_meds():
    now = datetime.now().strftime("%H:%M")
    if now == ROUTINES["meds"]["time"]:
        notify(ROUTINES["meds"]["message"], title=ROUTINES["meds"]["title"])
        print(f"[{now}] Meds reminder sent.")

def check_sleep():
    now = datetime.now().strftime("%H:%M")
    if now == ROUTINES["sleep"]["time"]:
        notify(ROUTINES["sleep"]["message"], title=ROUTINES["sleep"]["title"])
        print(f"[{now}] Sleep reminder sent.")

def check_calendar():
    events = get_todays_events()
    if not events:
        print("No events today.")
        return
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event.get("summary", "No title")
        notify(f"{start}: {summary}", title="Upcoming Class")
        print(f"Calendar event: {start} - {summary}")

def start_laundry_timer():
    minutes = ROUTINES["laundry"]["duration_minutes"]
    print(f"Laundry timer started for {minutes} minutes.")
    time.sleep(minutes * 60)
    notify(ROUTINES["laundry"]["message"], title=ROUTINES["laundry"]["title"])

def run_agent():
    print("LifeAgent started.")
    check_calendar()
    while True:
        check_meds()
        check_sleep()
        time.sleep(60)

if __name__ == "__main__":
    run_agent()