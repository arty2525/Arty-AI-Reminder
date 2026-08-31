from database import init_db, add_reminder
from recorder import record_wav
from speech_to_text import transcribe
from thai_parser import parse_thai_reminder
from tts import speak
from config import REMIND_BEFORE_MINUTES


def format_thai(dt):
    return dt.strftime("%d/%m/%Y %H:%M")


def main():
    init_db()
    print("AI Reminder พร้อมทำงาน")
    print("กด Enter เพื่อพูดคำสั่ง หรือพิมพ์ q เพื่อออก")

    while True:
        cmd = input("> ").strip().lower()
        if cmd == "q":
            break

        try:
            speak("กรุณาพูดคำสั่งตั้งเตือน")
            wav = record_wav()
            text = transcribe(wav)
            print("ข้อความที่ได้:", text)

            parsed = parse_thai_reminder(
                text,
                remind_before_minutes=REMIND_BEFORE_MINUTES,
            )
            reminder_id = add_reminder(
                parsed.event,
                parsed.event_time,
                parsed.remind_time,
            )

            print(f"บันทึก ID: {reminder_id}")
            print("กิจกรรม:", parsed.event)
            print("เวลาเข้าร่วม:", format_thai(parsed.event_time))
            print("เวลาแจ้งเตือน:", format_thai(parsed.remind_time))

            speak(
                f"บันทึกเรียบร้อย กิจกรรม {parsed.event} "
                f"จะแจ้งเตือนล่วงหน้า {REMIND_BEFORE_MINUTES} นาที"
            )
        except Exception as exc:
            print("เกิดข้อผิดพลาด:", exc)
            speak("ขออภัย ไม่สามารถบันทึกการเตือนได้ กรุณาลองใหม่")


if __name__ == "__main__":
    main()
