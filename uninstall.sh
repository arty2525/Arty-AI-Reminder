#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $EUID -ne 0 ]]; then
  echo "กรุณารัน: sudo ./uninstall.sh"
  exit 1
fi
systemctl disable --now arty-ai-reminder.service 2>/dev/null || true
rm -f /etc/systemd/system/arty-ai-reminder.service
rm -f /usr/local/bin/arty-reminder /usr/local/bin/arty-list /usr/local/bin/arty-test /usr/local/bin/arty-audio /usr/local/bin/arty-status
systemctl daemon-reload
printf 'ต้องการลบฐานข้อมูลและไฟล์ใน /opt/arty-ai-reminder ด้วยหรือไม่? [y/N] '
read -r ans
if [[ "$ans" =~ ^[Yy]$ ]]; then
  rm -rf /opt/arty-ai-reminder
else
  echo "เก็บข้อมูลไว้ที่ /opt/arty-ai-reminder"
fi
echo "Uninstall complete"
