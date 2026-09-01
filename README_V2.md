# Arty AI Reminder V2 — Hardware Prototype

V2 เพิ่ม **Push Button + LED 3 สี + Buzzer + DS3231 RTC (optional)** บน Raspberry Pi 4/5 + Ubuntu 24.04 ARM64

## ติดตั้งใหม่จาก GitHub

```bash
sudo apt update
sudo apt install -y git
cd ~
git clone https://github.com/arty2525/Arty-AI-Reminder.git
cd Arty-AI-Reminder
sudo bash install-v2.sh
sudo reboot
```

หลัง reboot:

```bash
arty-audio
arty-gpio-test
arty-v2-status
```

## การใช้งานแบบปุ่มจริง

เมื่อ service ทำงาน:

1. LED เขียวติด = พร้อม
2. กด Push Button GPIO17 หนึ่งครั้ง
3. LED เหลืองติด
4. ระบบพูด `กรุณาพูดคำสั่งตั้งเตือน`
5. พูด เช่น `ตั้งเตือน วันที่ 5 กันยายน เวลา 9 โมง ประชุมครู`
6. Whisper ถอดเสียงและบันทึก SQLite
7. LED เหลืองดับ และ LED เขียวกลับมาติด
8. ก่อนกิจกรรม 30 นาที LED แดง+Buzzer แจ้งเตือน แล้วระบบพูดชื่อกิจกรรม

## Pin Map

- Button: GPIO17
- Green LED: GPIO27
- Yellow LED: GPIO22
- Red LED: GPIO23
- Active Buzzer signal: GPIO24
- DS3231 SDA: GPIO2
- DS3231 SCL: GPIO3

รายละเอียดการต่อ: `docs/HARDWARE_V2.md`

## คำสั่ง

```bash
arty-audio       # ไมโครโฟน/ลำโพง
arty-gpio-test   # LED + buzzer + button
arty-v2-status   # สถานะ 2 services
arty-list        # รายการเตือน
arty-test        # เตือนทดสอบอีก 1 นาที
```

## Logs

```bash
journalctl -u arty-ai-button.service -f
journalctl -u arty-ai-reminder.service -f
```

## DS3231 RTC

```bash
cd ~/Arty-AI-Reminder
sudo bash scripts/enable_rtc_ds3231.sh
sudo reboot
sudo hwclock -r
```

ดู `docs/RTC_DS3231.md`

## อัปเกรดเครื่องที่ติดตั้ง V1 แล้ว

```bash
cd ~/Arty-AI-Reminder
git pull
sudo bash install-v2.sh
sudo reboot
```
