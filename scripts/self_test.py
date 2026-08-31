#!/usr/bin/env python3
from datetime import datetime
import sys
sys.path.insert(0, 'src')
from thai_parser import parse_thai_reminder

cases = [
    ("ตั้งเตือน วันที่ 1 กันยายน เวลา 08.00 น. ร่วมงานสถาปนา", "2026-09-01T08:00", "2026-09-01T07:30"),
    ("ตั้งเตือนวันที่ 1 กันยายน 2569 เวลา 8:00 ประชุมครู", "2026-09-01T08:00", "2026-09-01T07:30"),
    ("ตั้งเตือน วันที่ ๑ กันยายน ๒๕๖๙ เวลา ๐๘.๓๐ น. ทดสอบเลขไทย", "2026-09-01T08:30", "2026-09-01T08:00"),
]
for text, event_iso, reminder_iso in cases:
    p = parse_thai_reminder(text, now=datetime(2026,8,31,12,0))
    assert p.event_time.isoformat(timespec='minutes') == event_iso
    assert p.remind_time.isoformat(timespec='minutes') == reminder_iso
print(f"PASS: {len(cases)} parser tests")
