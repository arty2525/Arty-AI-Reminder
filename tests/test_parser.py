import unittest
from datetime import datetime
import sys
sys.path.insert(0, 'src')
from thai_parser import parse_thai_reminder

class ThaiParserTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 8, 31, 12, 0)

    def test_standard_command(self):
        p = parse_thai_reminder(
            'ตั้งเตือน วันที่ 1 กันยายน เวลา 08.00 น. ร่วมงานสถาปนา',
            now=self.now,
        )
        self.assertEqual(p.event, 'ร่วมงานสถาปนา')
        self.assertEqual(p.event_time, datetime(2026, 9, 1, 8, 0))
        self.assertEqual(p.remind_time, datetime(2026, 9, 1, 7, 30))

    def test_buddhist_year(self):
        p = parse_thai_reminder(
            'ตั้งเตือนวันที่ 1 กันยายน 2569 เวลา 8:00 ประชุมครู',
            now=self.now,
        )
        self.assertEqual(p.event_time.year, 2026)

    def test_thai_digits(self):
        p = parse_thai_reminder(
            'ตั้งเตือน วันที่ ๑ กันยายน ๒๕๖๙ เวลา ๐๘.๓๐ น. ทดสอบเลขไทย',
            now=self.now,
        )
        self.assertEqual(p.event_time, datetime(2026, 9, 1, 8, 30))

if __name__ == '__main__':
    unittest.main()
