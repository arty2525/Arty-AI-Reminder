import time
from datetime import datetime
from database import init_db, get_due_reminders, mark_notified, mark_missed_before
from tts import speak
from config import CHECK_INTERVAL_SECONDS


def main():
    init_db()
    print("Reminder daemon started")

    while True:
        now = datetime.now()
        mark_missed_before(now)
        for row in get_due_reminders(now):
            event_time = datetime.fromisoformat(row["event_time"])
            minutes_left = max(0, round((event_time - now).total_seconds() / 60))
            message = (
                f"แจ้งเตือน อีก {minutes_left} นาที "
                f"มีกิจกรรม {row['event']} เวลา {event_time.strftime('%H:%M')}"
            )
            print(message)
            speak(message)
            mark_notified(row["id"])
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
