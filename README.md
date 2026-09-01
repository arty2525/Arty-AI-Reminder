# Arty AI Reminder

Prototype ผู้ช่วย AI แจ้งเตือนด้วยเสียงภาษาไทยสำหรับ **Raspberry Pi + Ubuntu**

ผู้ใช้สามารถพูด เช่น

> ตั้งเตือน วันที่ 1 กันยายน เวลา 08.00 น. ร่วมงานสถาปนา

ระบบใช้ `whisper.cpp` ถอดเสียงภาษาไทย, แปลงวันที่/เวลา, บันทึกลง SQLite และแจ้งเตือนล่วงหน้า **30 นาที**

## V2 — รุ่นแนะนำสำหรับ Prototype จริง

V2 เพิ่ม:

- Push Button กดเพื่อเริ่มพูด
- LED เขียว = พร้อม
- LED เหลือง = กำลังฟัง/ประมวลผล
- LED แดง + Buzzer = แจ้งเตือน
- DS3231 RTC แบบเลือกติดตั้ง เพื่อรักษาเวลาเมื่อไม่มี Internet
- ตรวจ Raspberry Pi 5 และแก้ compatibility ของ `gpiozero/lgpio` อัตโนมัติ

ติดตั้ง:

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

ดูรายละเอียด V2 ที่ `README_V2.md` และการต่อวงจรที่ `docs/HARDWARE_V2.md`

## Pin Map V2

| อุปกรณ์ | GPIO |
|---|---:|
| Push Button | GPIO17 |
| LED เขียว | GPIO27 |
| LED เหลือง | GPIO22 |
| LED แดง | GPIO23 |
| Active Buzzer signal | GPIO24 |
| DS3231 SDA | GPIO2 |
| DS3231 SCL | GPIO3 |

> GPIO ของ Raspberry Pi เป็นลอจิก 3.3V ห้ามป้อน 5V เข้าขา GPIO โดยตรง และ LED ต้องมีตัวต้านทาน 220–330Ω

## V1 — Software Prototype

หากยังไม่ต่อ GPIO สามารถติดตั้งเฉพาะ V1 ได้:

```bash
git clone https://github.com/arty2525/Arty-AI-Reminder.git
cd Arty-AI-Reminder
sudo ./install.sh
sudo reboot
```

คำสั่ง V1:

```bash
arty-audio       # ตรวจไมโครโฟน/ลำโพง
arty-reminder    # กด Enter แล้วพูดคำสั่งภาษาไทย
arty-test        # สร้างการเตือนทดสอบใน 1 นาที
arty-list        # ดูรายการใน SQLite
arty-status      # ดูสถานะ reminder daemon
```

## ตัวอย่าง

พูด:

```text
ตั้งเตือน วันที่ 1 กันยายน เวลา 08.00 น. ร่วมงานสถาปนา
```

ผล:

```text
กิจกรรม       : ร่วมงานสถาปนา
เวลาเข้าร่วม   : 01/09/2026 08:00
เวลาแจ้งเตือน  : 01/09/2026 07:30
```

## โครงสร้างหลัก

```text
Arty-AI-Reminder/
├── README.md
├── README_V2.md
├── install.sh
├── install-v2.sh
├── update.sh
├── uninstall.sh
├── src/
│   ├── voice_assistant.py
│   ├── voice_once.py
│   ├── recorder.py
│   ├── speech_to_text.py
│   ├── thai_parser.py
│   ├── database.py
│   ├── hardware.py
│   ├── button_daemon_v2.py
│   ├── reminder_daemon_v2.py
│   ├── tts.py
│   └── config.py
├── cloud-init/
├── docs/
│   ├── HARDWARE_V2.md
│   └── RTC_DS3231.md
├── scripts/
│   ├── gpio_test.py
│   ├── pi5_gpio_fix.sh
│   └── enable_rtc_ds3231.sh
├── tests/
└── .github/workflows/
```

## DS3231 RTC

หลังต่อ DS3231 แล้ว:

```bash
cd ~/Arty-AI-Reminder
sudo bash scripts/enable_rtc_ds3231.sh
sudo reboot
sudo hwclock -r
```

Ubuntu บน Raspberry Pi ใช้ boot configuration ที่ `/boot/firmware/config.txt`; สคริปต์จะเพิ่ม `dtparam=i2c_arm=on` และ `dtoverlay=i2c-rtc,ds3231` เมื่อยังไม่มี

## อัปเกรด V1 → V2

```bash
cd ~/Arty-AI-Reminder
git pull
sudo bash install-v2.sh
sudo reboot
```

## ทดสอบ Source Code

```bash
python3 -m unittest discover -s tests -v
python3 scripts/self_test.py
```

GitHub Actions ตรวจทั้ง Python tests และ syntax ของ Python/Shell scripts ทุกครั้งที่ push

## SD Card / Classroom

ดู `docs/INSTALL_SD.md` สำหรับการเตรียม Ubuntu ลง microSD และ `cloud-init/` สำหรับตัวอย่างการติดตั้งอัตโนมัติในบูตแรก

## License

MIT
