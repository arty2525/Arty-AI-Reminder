# Arty AI Reminder V2 — การต่อวงจรจริง

## ขาที่กำหนด (BCM)

| อุปกรณ์ | GPIO | Physical pin | การต่อ |
|---|---:|---:|---|
| Push Button | GPIO17 | Pin 11 | ขาหนึ่งเข้า GPIO17 อีกขาเข้า GND |
| LED เขียว | GPIO27 | Pin 13 | GPIO27 → R 220–330Ω → Anode LED, Cathode → GND |
| LED เหลือง | GPIO22 | Pin 15 | GPIO22 → R 220–330Ω → Anode LED, Cathode → GND |
| LED แดง | GPIO23 | Pin 16 | GPIO23 → R 220–330Ω → Anode LED, Cathode → GND |
| Active Buzzer signal | GPIO24 | Pin 18 | ใช้ buzzer module 3.3V-compatible หรือขับผ่าน transistor |
| DS3231 SDA | GPIO2 / SDA1 | Pin 3 | SDA |
| DS3231 SCL | GPIO3 / SCL1 | Pin 5 | SCL |
| DS3231 VCC | — | Pin 1 | 3.3V แนะนำสำหรับโมดูลที่รองรับ |
| DS3231 GND | — | Pin 6 | GND |

> **ข้อควรระวัง:** GPIO ของ Raspberry Pi เป็นลอจิก 3.3V ห้ามป้อน 5V เข้าขา GPIO โดยตรง และ LED ต้องมีตัวต้านทานอนุกรมทุกดวง

## ความหมาย LED

- **เขียวติดค้าง**: ระบบพร้อมรับคำสั่ง
- **เหลืองติด**: กำลังบันทึกเสียง/ถอดเสียง/ประมวลผล
- **แดงกระพริบ + Buzzer**: ถึงเวลาแจ้งเตือน

## ปุ่มกด

โปรแกรมเปิด internal pull-up ดังนั้นต่อปุ่มเพียงสองสาย:

```text
GPIO17 (Pin 11) ----[ Push Button ]---- GND (Pin 9 หรือ Pin 6)
```

เมื่อกดปุ่ม โปรแกรมจะเรียก `voice_assistant.py --once` อัตโนมัติ

## LED

ตัวอย่าง LED เขียว:

```text
GPIO27 ----[ 220–330Ω ]----|>|---- GND
                            LED
```

ทำเหมือนกันกับ LED เหลือง GPIO22 และ LED แดง GPIO23

## Buzzer

แนะนำใช้ **Active Buzzer Module** ที่มีขา `SIG/VCC/GND` และรับสัญญาณ 3.3V ได้ โดยต่อ `SIG → GPIO24` หากเป็น buzzer เปล่าหรือกินกระแสสูง ให้ใช้ transistor driver ห้ามดึงกระแสสูงจาก GPIO โดยตรง

## ทดสอบ GPIO หลังติดตั้ง

```bash
arty-gpio-test
```

ระบบจะทดสอบ LED เขียว → เหลือง → แดง+Buzzer แล้วให้นักเรียนกดปุ่มภายใน 10 วินาที

## เปิดใช้ DS3231

ต่อโมดูลให้เรียบร้อย แล้วรัน:

```bash
cd ~/Arty-AI-Reminder
sudo bash scripts/enable_rtc_ds3231.sh
sudo reboot
```

หลังบูต:

```bash
ls -l /dev/rtc*
sudo hwclock -r
sudo i2cdetect -y 1
```

ถ้าเวลาระบบถูกต้องและต้องการบันทึกเวลาปัจจุบันลง RTC:

```bash
sudo hwclock --systohc
```

## Service ของ V2

```bash
systemctl status arty-ai-reminder.service
systemctl status arty-ai-button.service
```

ดู log ปุ่มแบบสด:

```bash
journalctl -u arty-ai-button.service -f
```
