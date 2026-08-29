import os
import time
from datetime import datetime

def notify_safe(message, title="LifeAgent"):
    try:
        from ntfy import notify
        notify(message, title=title)
        return True
    except Exception as e:
        print(f"Notify failed: {type(e).__name__}")
        return False

ROUTINES = {
    "meds": {"time": "08:00", "message": "Time to take your meds!", "title": "Meds Reminder"},
    "sleep": {"time": "23:00", "message": "Bedtime soon — wind down", "title": "Sleep Reminder"},
}

last_reminder_sent = {}
last_calendar_check = None

def check_meds():
    now = datetime.now().strftime("%H:%M")
    key = "meds_" + now[:10]
    if now == ROUTINES["meds"]["time"] and key not in last_reminder_sent:
        sent = notify_safe(ROUTINES["meds"]["message"], title=ROUTINES["meds"]["title"])
        if sent:
            last_reminder_sent[key] = True
            print(f"[{now}] Meds reminder sent.")
        else:
            print(f"[{now}] Meds reminder FAILED.")

def check_sleep():
    now = datetime.now().strftime("%H:%M")
    key = "sleep_" + now[:10]
    if now == ROUTINES["sleep"]["time"] and key not in last_reminder_sent:
        sent = notify_safe(ROUTINES["sleep"]["message"], title=ROUTINES["sleep"]["title"])
        if sent:
            last_reminder_sent[key] = True
            print(f"[{now}] Sleep reminder sent.")
        else:
            print(f"[{now}] Sleep reminder FAILED.")

def check_calendar():
    global last_calendar_check
    today = datetime.now().date()
    if last_calendar_check == today:
        return
    try:
        from calendar_tool import get_todays_events
        events = get_todays_events()
        last_calendar_check = today
        if not events:
            print("No events today.")
            return
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "No title")
            notify_safe(f"{start}: {summary}", title="Today's Schedule")
            print(f"Calendar event: {start} - {summary}")
    except Exception as e:
        print(f"Calendar check failed: {type(e).__name__} — reminders still active")

def run_agent():
    print("LifeAgent started.")
    check_calendar()
    while True:
        check_meds()
        check_sleep()
        now_minute = datetime.now().strftime("%H:%M")
        if now_minute == "00:01":
            check_calendar()
        time.sleep(55)

if __name__ == "__main__":
    run_agent()