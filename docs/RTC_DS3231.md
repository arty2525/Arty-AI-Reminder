# DS3231 RTC สำหรับ Arty AI Reminder

DS3231 เป็นอุปกรณ์เสริมสำหรับรักษาเวลาของ Raspberry Pi เมื่อไม่มี Internet/NTP

## การต่อสาย

| DS3231 | Raspberry Pi |
|---|---|
| SDA | GPIO2 / Pin 3 |
| SCL | GPIO3 / Pin 5 |
| GND | GND / Pin 6 |
| VCC | 3.3V / Pin 1 สำหรับโมดูลที่รองรับ |

## เปิดใช้งานบน Ubuntu

```bash
cd ~/Arty-AI-Reminder
sudo bash scripts/enable_rtc_ds3231.sh
sudo reboot
```

สคริปต์จะตรวจและเพิ่มบรรทัดต่อไปนี้ใน `/boot/firmware/config.txt` เฉพาะเมื่อยังไม่มี:

```text
dtparam=i2c_arm=on
dtoverlay=i2c-rtc,ds3231
```

## ตรวจหลัง reboot

```bash
ls -l /dev/rtc*
sudo hwclock -r
sudo i2cdetect -y 1
```

ถ้าเวลาระบบปัจจุบันถูกต้อง ให้เขียนลง RTC:

```bash
sudo hwclock --systohc
```

## หมายเหตุ

อย่าตั้งเวลา RTC จากเครื่องที่เวลาระบบยังผิด เพราะจะทำให้ DS3231 จำเวลาผิดตามไปด้วย
