from database import init_db, list_reminders


def main():
    init_db()
    rows = list_reminders()
    if not rows:
        print("ยังไม่มีรายการเตือน")
        return
    print("ID | กิจกรรม | เวลาเข้าร่วม | เวลาเตือน | สถานะ")
    print("-" * 80)
    for r in rows:
        print(f"{r['id']} | {r['event']} | {r['event_time']} | {r['remind_time']} | {r['status']}")


if __name__ == "__main__":
    main()
