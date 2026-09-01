#!/usr/bin/env bash
set -Eeuo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="/opt/arty-ai-reminder"
TARGET_USER="${ARTY_USER:-${SUDO_USER:-ubuntu}}"
if ! id "$TARGET_USER" >/dev/null 2>&1; then
  FIRST_USER="$(getent passwd 1000 | cut -d: -f1 || true)"
  TARGET_USER="${FIRST_USER:-root}"
fi
TARGET_GROUP="$(id -gn "$TARGET_USER")"

if [[ $EUID -ne 0 ]]; then
  echo "กรุณารัน: sudo bash install-v2.sh"
  exit 1
fi

printf '\n=== Arty AI Reminder V2 Hardware Installer ===\n'

# Install/refresh the stable V1 core first. It also copies every src/*.py,
# including V2 modules, into /opt/arty-ai-reminder.
echo "[1/7] ติดตั้ง Core AI Reminder"
bash "$REPO_DIR/install.sh"

echo "[2/7] ติดตั้ง GPIO/I2C packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3-gpiozero python3-lgpio i2c-tools

echo "[3/7] ตั้งสิทธิ์ GPIO"
getent group gpio >/dev/null || groupadd gpio
usermod -aG gpio "$TARGET_USER" || true
cat > /etc/udev/rules.d/60-arty-gpio.rules <<'EOF'
SUBSYSTEM=="gpio", KERNEL=="gpiochip*", GROUP="gpio", MODE="0660"
EOF
udevadm control --reload-rules || true
udevadm trigger --subsystem-match=gpio || true
for chip in /dev/gpiochip*; do
  [[ -e "$chip" ]] || continue
  chgrp gpio "$chip" || true
  chmod 0660 "$chip" || true
done

# Keep a copy of the classroom GPIO self-test beside the installed app.
install -m 0644 "$REPO_DIR/scripts/gpio_test.py" "$APP_DIR/gpio_test.py"
chown "$TARGET_USER:$TARGET_GROUP" "$APP_DIR/gpio_test.py"

echo "[4/7] ติดตั้งคำสั่งทดสอบฮาร์ดแวร์"
cat > /usr/local/bin/arty-gpio-test <<'SH'
#!/usr/bin/env bash
cd /opt/arty-ai-reminder
export GPIOZERO_PIN_FACTORY=lgpio
exec python3 gpio_test.py "$@"
SH
cat > /usr/local/bin/arty-v2-status <<'SH'
#!/usr/bin/env bash
echo '=== Reminder daemon ==='
systemctl --no-pager --full status arty-ai-reminder.service || true
echo
echo '=== Push-button daemon ==='
systemctl --no-pager --full status arty-ai-button.service || true
SH
chmod 0755 /usr/local/bin/arty-gpio-test /usr/local/bin/arty-v2-status

echo "[5/7] เปิด Reminder daemon V2 (LED แดง + Buzzer)"
cat > /etc/systemd/system/arty-ai-reminder.service <<EOF
[Unit]
Description=Arty AI Reminder V2 Daemon
After=local-fs.target sound.target

[Service]
Type=simple
User=$TARGET_USER
Group=$TARGET_GROUP
SupplementaryGroups=audio gpio
WorkingDirectory=$APP_DIR
Environment=GPIOZERO_PIN_FACTORY=lgpio
ExecStart=/usr/bin/python3 $APP_DIR/reminder_daemon_v2.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "[6/7] เปิด Push-button daemon V2"
cat > /etc/systemd/system/arty-ai-button.service <<EOF
[Unit]
Description=Arty AI Reminder V2 Push Button
After=local-fs.target sound.target arty-ai-reminder.service

[Service]
Type=simple
User=$TARGET_USER
Group=$TARGET_GROUP
SupplementaryGroups=audio gpio
WorkingDirectory=$APP_DIR
Environment=GPIOZERO_PIN_FACTORY=lgpio
ExecStart=/usr/bin/python3 $APP_DIR/button_daemon_v2.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable arty-ai-reminder.service arty-ai-button.service
systemctl restart arty-ai-reminder.service
systemctl restart arty-ai-button.service

echo "[7/7] ตรวจ Syntax และสถานะ"
python3 -m py_compile "$APP_DIR"/*.py
systemctl --no-pager --full status arty-ai-reminder.service || true
systemctl --no-pager --full status arty-ai-button.service || true

echo
printf '%s\n' '============================================================'
printf '%s\n' ' Arty AI Reminder V2 installed'
printf '%s\n' '============================================================'
echo "ทดสอบเสียง        : arty-audio"
echo "ทดสอบ GPIO        : arty-gpio-test"
echo "ดูสถานะ V2        : arty-v2-status"
echo "ดูรายการเตือน     : arty-list"
echo "ทดสอบเตือน 1 นาที: arty-test"
echo
echo "แนะนำ reboot 1 ครั้งเพื่อให้ group/udev permissions สมบูรณ์:"
echo "  sudo reboot"
echo
echo "DS3231 เป็นอุปกรณ์เสริม เปิดใช้ภายหลังด้วย:"
echo "  sudo bash scripts/enable_rtc_ds3231.sh"
