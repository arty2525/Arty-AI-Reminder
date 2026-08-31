# การเตรียม Ubuntu microSD สำหรับ Raspberry Pi

## วิธีที่แนะนำ

1. ใช้ Raspberry Pi Imager
2. เลือก Ubuntu Server 24.04 LTS 64-bit สำหรับ Raspberry Pi
3. Write ลง microSD
4. เปิด Raspberry Pi และเชื่อม Internet
5. Login เข้า Ubuntu
6. Clone repository แล้วรัน installer

```bash
git clone https://github.com/arty2525/Arty-AI-Reminder.git
cd Arty-AI-Reminder
sudo ./install.sh
sudo reboot
```

หลัง reboot:

```bash
arty-audio
arty-test
arty-reminder
```

## การสร้าง Master SD สำหรับห้องเรียน

เมื่อทดสอบ Raspberry Pi ต้นแบบจนสมบูรณ์แล้ว สามารถ shutdown และ clone microSD เป็น Master Image เพื่อนำไปแฟลชให้ชุดนักเรียนหลายชุดได้

ข้อควรระวัง: อย่าฝัง Wi-Fi password, SSH private key หรือข้อมูลส่วนบุคคลลงใน public GitHub repository หรือ Master Image ที่แจกนักเรียน
