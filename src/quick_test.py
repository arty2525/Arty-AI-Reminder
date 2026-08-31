from datetime import datetime, timedelta
from database import init_db, add_reminder


def main():
    init_db()
    now = datetime.now().replace(microsecond=0)
    event_time = now + timedelta(minutes=2)
    remind_time = now + timedelta(minutes=1)
    reminder_id = add_reminder('ทดสอบระบบ AI Reminder', event_time, remind_time)
    print(f'สร้างรายการทดสอบ ID {reminder_id}')
    print(f'เวลาแจ้งเตือน : {remind_time:%H:%M:%S}')
    print(f'เวลากิจกรรม   : {event_time:%H:%M:%S}')
    print('เมื่อถึงเวลา ระบบควรพูดแจ้งเตือนผ่านลำโพง')


if __name__ == '__main__':
    main()
