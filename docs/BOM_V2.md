# BOM — Arty AI Reminder V2 (ต่อ 1 ชุด)

## อุปกรณ์หลัก

| รายการ | จำนวน | หมายเหตุ |
|---|---:|---|
| Raspberry Pi 4 หรือ Pi 5 | 1 | RAM 4 GB ขึ้นไปแนะนำ |
| microSD 64 GB | 1 | Class 10 / A1 หรือดีกว่า |
| Power Supply ตามรุ่น Pi | 1 | ใช้กำลังไฟตามสเปกของบอร์ด |
| USB Microphone | 1 | ALSA มองเห็นได้ |
| USB Speaker | 1 | หรืออุปกรณ์เสียง USB ที่รองรับ Linux |
| Breadboard | 1 | สำหรับ Prototype |
| Push Button | 1 | Normally open |
| LED เขียว | 1 | 5 mm |
| LED เหลือง | 1 | 5 mm |
| LED แดง | 1 | 5 mm |
| R 220–330Ω | 3 | สำหรับ LED แต่ละดวง |
| Active Buzzer Module | 1 | Signal 3.3V-compatible แนะนำ |
| Jumper wire | 15–20 | Female/Male ตามอุปกรณ์ |
| DS3231 RTC | 1 | Optional แต่แนะนำสำหรับระบบจริง |

## อุปกรณ์เสริมสำหรับความปลอดภัยของ Buzzer

ถ้าใช้ buzzer เปล่าหรือ buzzer ที่กินกระแสมากกว่าที่ GPIO ควรขับโดยตรง ให้เพิ่ม:

- NPN transistor เช่น 2N2222 / BC547 จำนวน 1
- R base 1kΩ จำนวน 1
- Diode สำหรับโหลดเชิงเหนี่ยวนำตามชนิดอุปกรณ์

สำหรับห้องเรียน แนะนำ **Active Buzzer Module ที่มีวงจร driver ในตัว** จะต่อและสอนได้ง่ายกว่า

## ชุดที่ต้องเตรียมต่อกลุ่ม

ตัวอย่างห้องเรียน 8 กลุ่ม:

- Raspberry Pi 8 ชุด
- microSD 8 ใบ
- USB Microphone 8 ตัว
- USB Speaker 8 ตัว
- Breadboard 8 แผง
- Push Button 8 ตัว
- LED รวม 24 ดวง
- R 220–330Ω อย่างน้อย 24 ตัว
- Active Buzzer Module 8 ตัว
- DS3231 จำนวน 8 ตัว (ถ้าเรียน RTC)

ควรมีอะไหล่สำรอง LED, ตัวต้านทาน, jumper และ microSD อย่างน้อย 10–20%
