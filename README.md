# Arty AI Reminder

Prototype ผู้ช่วย AI แจ้งเตือนด้วยเสียงภาษาไทยสำหรับ **Raspberry Pi + Ubuntu**

ผู้ใช้สามารถพูด เช่น

> ตั้งเตือน วันที่ 1 กันยายน เวลา 08.00 น. ร่วมงานสถาปนา

ระบบจะถอดเสียงภาษาไทยด้วย `whisper.cpp`, แปลงวันที่/เวลา, บันทึกลง SQLite และแจ้งเตือนล่วงหน้า **30 นาที** ผ่านลำโพง

## เป้าหมายฮาร์ดแวร์

- Raspberry Pi 4 หรือ Raspberry Pi 5 (แนะนำ RAM 4 GB ขึ้นไป)
- Ubuntu 24.04 LTS Server ARM64
- microSD 32 GB ขึ้นไป (แนะนำ 64 GB)
- USB Microphone
- USB Speaker หรืออุปกรณ์เสียงที่ ALSA มองเห็น
- Internet สำหรับการติดตั้งครั้งแรก

## ติดตั้งจาก GitHub

```bash
git clone https://github.com/arty2525/Arty-AI-Reminder.git
cd Arty-AI-Reminder
sudo ./install.sh
```

หลังติดตั้ง แนะนำ reboot 1 ครั้ง:

```bash
sudo reboot
```

## คำสั่งหลัก

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

ผลที่ควรได้:

```text
กิจกรรม       : ร่วมงานสถาปนา
เวลาเข้าร่วม   : 01/09/2026 08:00
เวลาแจ้งเตือน  : 01/09/2026 07:30
```

## โครงสร้าง

```text
Arty-AI-Reminder/
├── README.md
├── install.sh
├── update.sh
├── uninstall.sh
├── src/
│   ├── voice_assistant.py
│   ├── recorder.py
│   ├── speech_to_text.py
│   ├── thai_parser.py
│   ├── database.py
│   ├── reminder_daemon.py
│   ├── tts.py
│   └── config.py
├── cloud-init/
├── docs/
├── scripts/
├── tests/
└── .github/workflows/
```

## อัปเดตโปรแกรมบน Raspberry Pi

```bash
cd ~/Arty-AI-Reminder
git pull
sudo ./update.sh
```

หากมีการเปลี่ยน dependency หรือ `whisper.cpp` ให้ใช้

```bash
sudo ./install.sh
```

อีกครั้งได้ โดย installer ออกแบบให้รันซ้ำได้

## ทดสอบ Source Code ก่อนติดตั้ง

```bash
python3 -m unittest discover -s tests -v
python3 scripts/self_test.py
```

## SD Card / Classroom

ดู `docs/INSTALL_SD.md` สำหรับการเตรียม Ubuntu ลง microSD และ `cloud-init/` สำหรับตัวอย่างการติดตั้งอัตโนมัติในบูตแรก

## หมายเหตุด้านเสียง

อุปกรณ์ USB microphone/speaker แต่ละรุ่นอาจได้หมายเลข ALSA ต่างกัน ให้เริ่มตรวจจาก

```bash
arty-audio
```

หาก `arecord` หรือ `aplay` ไม่เลือกอุปกรณ์ที่ต้องการเป็นค่าเริ่มต้น อาจต้องกำหนด ALSA default device เพิ่มตามฮาร์ดแวร์ที่ใช้ในห้องเรียน

## License

MIT
