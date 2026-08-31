# cloud-init

โฟลเดอร์นี้เก็บตัวอย่างสำหรับทำ SD Card แบบ first-boot provisioning

- `user-data.example` เป็นตัวอย่างการ clone และติดตั้ง Arty AI Reminder อัตโนมัติ
- `network-config.example` เป็นตัวอย่างการตั้งค่า LAN/Wi-Fi

คำเตือน: อย่า commit Wi-Fi password, password hash, SSH private key หรือข้อมูลจริงของโรงเรียนลง public repository

สำหรับการใช้งานทั่วไป แนะนำให้ใช้ Ubuntu image ทางการ แล้ว clone repository + `sudo ./install.sh` เพราะดูแลและอัปเดตง่ายกว่า
