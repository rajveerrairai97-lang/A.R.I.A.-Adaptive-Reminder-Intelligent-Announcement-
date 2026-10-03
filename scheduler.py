import json
import os
import threading
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from notifier import notify
from personality import generate_reminder

REMINDERS_FILE = "reminders.json"

IST = ZoneInfo("Asia/Kolkata")

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}


def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []

    try:
        with open(REMINDERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        return []


def save_reminders(reminders):
    with open(REMINDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            reminders,
            file,
            indent=4,
            ensure_ascii=False
        )


def generate_id(reminders):
    if not reminders:
        return 1

    ids = []

    for reminder in reminders:
        try:
            ids.append(int(reminder.get("id", 0)))
        except Exception:
            pass

    return max(ids, default=0) + 1


def create_reminder(
    task,
    reminder_time,
    reminder_date=None,
    recurrence="once",
    weekdays=None
):
    reminders = load_reminders()

    reminder = {
        "id": generate_id(reminders),
        "task": task,
        "time": reminder_time.strftime("%H:%M"),
        "date": reminder_date.isoformat() if reminder_date else None,
        "recurrence": recurrence,
        "weekdays": weekdays or [],
        "triggered_dates": [],
        "active": True,
        "created_at": datetime.now(IST).isoformat()
    }

    reminders.append(reminder)

    save_reminders(reminders)

    return reminder


def delete_reminder(reminder_id):
    reminders = load_reminders()

    for reminder in reminders:
        if int(reminder.get("id", -1)) == int(reminder_id):
            reminder["active"] = False
            save_reminders(reminders)
            return True

    return False


def restore_reminder(reminder_id):
    reminders = load_reminders()

    for reminder in reminders:
        if int(reminder.get("id", -1)) == int(reminder_id):
            reminder["active"] = True
            save_reminders(reminders)
            return True

    return False


def clear_old_trigger_records(reminder):
    today = datetime.now(IST).date()

    cleaned = []

    for value in reminder.get("triggered_dates", []):
        try:
            d = datetime.fromisoformat(value).date()

            if d >= today - timedelta(days=30):
                cleaned.append(value)

        except Exception:
            pass

    reminder["triggered_dates"] = cleaned


def should_trigger(reminder, now):
    if not reminder.get("active", True):
        return False

    current_date = now.date()
    current_time = now.strftime("%H:%M")

    if reminder.get("time") != current_time:
        return False

    triggered_dates = reminder.get("triggered_dates", [])

    today_string = current_date.isoformat()

    if today_string in triggered_dates:
        return False

    recurrence = reminder.get("recurrence", "once")

    # ----------------------------------------
    # ONE-TIME REMINDER
    # ----------------------------------------

    if recurrence == "once":

        reminder_date = reminder.get("date")

        if not reminder_date:
            return False

        if reminder_date != today_string:
            return False

        return True

    # ----------------------------------------
    # EVERY DAY
    # ----------------------------------------

    if recurrence == "daily":
        return True

    # ----------------------------------------
    # SELECTED WEEKDAYS
    # ----------------------------------------

    if recurrence == "weekly":

        weekdays = reminder.get("weekdays", [])

        current_weekday = now.weekday()

        for day in weekdays:

            if isinstance(day, str):
                day_number = WEEKDAYS.get(day.lower())

                if day_number == current_weekday:
                    return True

            else:
                try:
                    if int(day) == current_weekday:
                        return True
                except Exception:
                    pass

    return False


def trigger_reminder(reminder):
    task = reminder.get("task", "your task")

    message = generate_reminder(task)

    notify(
        message,
        title="🔷 JARVIS REMINDER"
    )


def check_reminders():
    reminders = load_reminders()

    now = datetime.now(IST)

    changed = False

    for reminder in reminders:

        clear_old_trigger_records(reminder)

        if should_trigger(reminder, now):

            print()
            print("🤖 REMINDER TRIGGERED")
            print(f"   Task: {reminder.get('task')}")
            print(f"   Time: {reminder.get('time')}")

            trigger_reminder(reminder)

            today_string = now.date().isoformat()

            reminder.setdefault(
                "triggered_dates",
                []
            ).append(today_string)

            changed = True

            # One-time reminder becomes inactive
            if reminder.get("recurrence") == "once":
                reminder["active"] = False

    if changed:
        save_reminders(reminders)


def scheduler_loop():
    print()
    print("=" * 65)
    print("🤖 JARVIS SCHEDULER ONLINE")
    print("🇮🇳 Timezone: Asia/Kolkata")
    print("=" * 65)

    last_minute = None

    while True:

        try:
            now = datetime.now(IST)

            current_minute = now.strftime(
                "%Y-%m-%d %H:%M"
            )

            if current_minute != last_minute:

                last_minute = current_minute

                check_reminders()

            time.sleep(1)

        except Exception as error:

            print(
                f"[SCHEDULER ERROR] {error}"
            )

            time.sleep(5)


def start_scheduler():

    thread = threading.Thread(
        target=scheduler_loop,
        daemon=True
    )

    thread.start()

    return thread