#!/usr/bin/env bash
set -Eeuo pipefail

CONFIG=/boot/firmware/config.txt

if [[ $EUID -ne 0 ]]; then
  echo "กรุณารัน: sudo bash scripts/enable_rtc_ds3231.sh"
  exit 1
fi

if [[ ! -f "$CONFIG" ]]; then
  echo "ไม่พบ $CONFIG — สคริปต์นี้ออกแบบสำหรับ Ubuntu บน Raspberry Pi"
  exit 1
fi

apt-get update
apt-get install -y i2c-tools

append_if_missing() {
  local line="$1"
  if ! grep -Fxq "$line" "$CONFIG"; then
    printf '\n%s\n' "$line" >> "$CONFIG"
    echo "เพิ่ม: $line"
  else
    echo "มีอยู่แล้ว: $line"
  fi
}

append_if_missing "dtparam=i2c_arm=on"
append_if_missing "dtoverlay=i2c-rtc,ds3231"

echo
echo "ตั้งค่า DS3231 แล้ว ต้อง reboot 1 ครั้ง:"
echo "  sudo reboot"
echo
echo "หลัง reboot ตรวจด้วย:"
echo "  ls -l /dev/rtc*"
echo "  sudo hwclock -r"
echo "  sudo i2cdetect -y 1"
echo
echo "หากเวลาระบบถูกต้องและต้องการเขียนลง RTC:"
echo "  sudo hwclock --systohc"
