import re
from dataclasses import dataclass
from datetime import datetime, timedelta

MONTHS = {
    "มกราคม": 1,
    "กุมภาพันธ์": 2,
    "มีนาคม": 3,
    "เมษายน": 4,
    "พฤษภาคม": 5,
    "มิถุนายน": 6,
    "กรกฎาคม": 7,
    "สิงหาคม": 8,
    "กันยายน": 9,
    "ตุลาคม": 10,
    "พฤศจิกายน": 11,
    "ธันวาคม": 12,
}

THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


@dataclass
class ParsedReminder:
    event: str
    event_time: datetime
    remind_time: datetime


def normalize(text: str) -> str:
    text = text.translate(THAI_DIGITS)
    text = text.replace("นาฬิกา", "น.")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_thai_reminder(text: str, now=None, remind_before_minutes=30):
    """Parse the classroom V1 command pattern.

    Examples:
      ตั้งเตือน วันที่ 1 กันยายน เวลา 08.00 น. ร่วมงานสถาปนา
      ตั้งเตือนวันที่ 1 กันยายน 2569 เวลา 8:00 ประชุมครู
    """
    now = now or datetime.now()
    text = normalize(text)

    month_pattern = "|".join(MONTHS.keys())
    pattern = re.compile(
        rf"(?:ตั้งเตือน\s*)?วันที่\s*(\d{{1,2}})\s*({month_pattern})"
        rf"(?:\s*(?:พ\.?ศ\.?|ปี)?\s*(\d{{4}}))?"
        rf".*?เวลา\s*(\d{{1,2}})(?:[\.:](\d{{1,2}}))?"
        rf"\s*(?:น\.|โมง)?\s*(.*)$"
    )

    match = pattern.search(text)
    if not match:
        raise ValueError(
            "ไม่พบรูปแบบวัน/เวลา กรุณาพูด เช่น "
            "'ตั้งเตือน วันที่ 1 กันยายน เวลา 08.00 น. ร่วมงานสถาปนา'"
        )

    day = int(match.group(1))
    month = MONTHS[match.group(2)]
    year_text = match.group(3)
    hour = int(match.group(4))
    minute = int(match.group(5) or 0)
    event = match.group(6).strip(" .,-")

    if not event:
        event = "กิจกรรมที่ตั้งเตือน"

    if year_text:
        year = int(year_text)
        if year >= 2400:
            year -= 543
    else:
        year = now.year

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError("เวลาไม่ถูกต้อง")

    try:
        event_time = datetime(year, month, day, hour, minute)
    except ValueError as exc:
        raise ValueError(f"วันที่หรือเวลาไม่ถูกต้อง: {exc}") from exc

    if not year_text and event_time <= now:
        event_time = event_time.replace(year=year + 1)

    remind_time = event_time - timedelta(minutes=remind_before_minutes)
    return ParsedReminder(event, event_time, remind_time)
