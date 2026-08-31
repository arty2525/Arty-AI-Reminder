#!/usr/bin/env bash
set -Eeuo pipefail

APP_NAME="Arty AI Reminder"
APP_DIR="/opt/arty-ai-reminder"
WHISPER_DIR="/opt/whisper.cpp"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_USER="${ARTY_USER:-${SUDO_USER:-ubuntu}}"
if ! id "$TARGET_USER" >/dev/null 2>&1; then
  FIRST_USER="$(getent passwd 1000 | cut -d: -f1 || true)"
  TARGET_USER="${FIRST_USER:-root}"
fi
TARGET_GROUP="$(id -gn "$TARGET_USER")"
LOG_FILE="/var/log/arty-ai-reminder-install.log"

if [[ $EUID -ne 0 ]]; then
  echo "กรุณารัน: sudo ./install.sh"
  exit 1
fi

exec > >(tee -a "$LOG_FILE") 2>&1
trap 'echo "[ERROR] ติดตั้งไม่สำเร็จที่บรรทัด $LINENO ดู log: $LOG_FILE"' ERR

echo "============================================================"
echo " $APP_NAME installer"
echo "============================================================"
echo "User: $TARGET_USER"
echo "Repo: $REPO_DIR"

if ! [[ -f /etc/os-release ]]; then
  echo "ไม่พบ /etc/os-release"
  exit 1
fi
. /etc/os-release
if [[ "${ID:-}" != "ubuntu" ]]; then
  echo "คำเตือน: ชุดติดตั้งนี้ทดสอบเป้าหมาย Ubuntu 24.04 LTS บน Raspberry Pi"
fi

ARCH="$(dpkg --print-architecture 2>/dev/null || uname -m)"
case "$ARCH" in
  arm64|aarch64) ;;
  *) echo "คำเตือน: architecture=$ARCH (แนะนำ arm64 บน Raspberry Pi 4/5)" ;;
esac

echo "[1/9] ตั้ง Time zone Asia/Bangkok"
timedatectl set-timezone Asia/Bangkok

echo "[2/9] ติดตั้ง system packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y \
  python3 python3-venv python3-pip \
  alsa-utils espeak-ng espeak-ng-data \
  git cmake build-essential curl ca-certificates

echo "[3/9] เตรียมผู้ใช้และโฟลเดอร์"
getent group audio >/dev/null || groupadd audio
usermod -aG audio "$TARGET_USER" || true
install -d -m 0755 "$APP_DIR"
install -d -m 0775 -o "$TARGET_USER" -g "$TARGET_GROUP" "$APP_DIR/audio"

install -m 0644 "$REPO_DIR"/src/*.py "$APP_DIR/"
install -m 0644 "$REPO_DIR/src/requirements.txt" "$APP_DIR/requirements.txt"
chown -R "$TARGET_USER:$TARGET_GROUP" "$APP_DIR"

echo "[4/9] ติดตั้ง/อัปเดต whisper.cpp"
if [[ ! -d "$WHISPER_DIR/.git" ]]; then
  rm -rf "$WHISPER_DIR"
  git clone --depth 1 https://github.com/ggml-org/whisper.cpp.git "$WHISPER_DIR"
else
  git -C "$WHISPER_DIR" fetch --depth 1 origin master || true
  git -C "$WHISPER_DIR" reset --hard origin/master || true
fi
cmake -S "$WHISPER_DIR" -B "$WHISPER_DIR/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$WHISPER_DIR/build" -j"$(nproc)"

WHISPER_BIN="$WHISPER_DIR/build/bin/whisper-cli"
if [[ ! -x "$WHISPER_BIN" ]]; then
  echo "ไม่พบ whisper-cli หลัง build: $WHISPER_BIN"
  exit 1
fi

echo "[5/9] ดาวน์โหลด Whisper multilingual base model"
MODEL="$WHISPER_DIR/models/ggml-base.bin"
if [[ ! -s "$MODEL" ]]; then
  (cd "$WHISPER_DIR" && sh ./models/download-ggml-model.sh base)
fi
if [[ ! -s "$MODEL" ]]; then
  echo "ดาวน์โหลดโมเดลไม่สำเร็จ: $MODEL"
  exit 1
fi

echo "[6/9] สร้างฐานข้อมูล SQLite"
sudo -u "$TARGET_USER" python3 - <<PY
import sys
sys.path.insert(0, "$APP_DIR")
from database import init_db
init_db()
print("SQLite initialized")
PY

echo "[7/9] ติดตั้ง command shortcuts"
cat > /usr/local/bin/arty-reminder <<'SH'
#!/usr/bin/env bash
cd /opt/arty-ai-reminder && exec python3 voice_assistant.py "$@"
SH
cat > /usr/local/bin/arty-list <<'SH'
#!/usr/bin/env bash
cd /opt/arty-ai-reminder && exec python3 list_reminders.py "$@"
SH
cat > /usr/local/bin/arty-test <<'SH'
#!/usr/bin/env bash
cd /opt/arty-ai-reminder && exec python3 quick_test.py "$@"
SH
cat > /usr/local/bin/arty-audio <<'SH'
#!/usr/bin/env bash
echo '=== Capture devices (microphones) ==='
arecord -l || true
echo
echo '=== Playback devices (speakers) ==='
aplay -l || true
SH
cat > /usr/local/bin/arty-status <<'SH'
#!/usr/bin/env bash
systemctl --no-pager --full status arty-ai-reminder.service
SH
chmod 0755 /usr/local/bin/arty-reminder /usr/local/bin/arty-list /usr/local/bin/arty-test /usr/local/bin/arty-audio /usr/local/bin/arty-status

echo "[8/9] ติดตั้ง systemd service"
cat > /etc/systemd/system/arty-ai-reminder.service <<EOF_SERVICE
[Unit]
Description=Arty AI Reminder Daemon
After=local-fs.target sound.target

[Service]
Type=simple
User=$TARGET_USER
Group=$TARGET_GROUP
SupplementaryGroups=audio
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/reminder_daemon.py
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF_SERVICE
systemctl daemon-reload
systemctl enable --now arty-ai-reminder.service

echo "[9/9] ตรวจสอบการติดตั้ง"
python3 -m py_compile "$APP_DIR"/*.py
python3 - <<PY
import sys
sys.path.insert(0, "$APP_DIR")
from datetime import datetime
from thai_parser import parse_thai_reminder
p = parse_thai_reminder("ตั้งเตือน วันที่ 1 กันยายน 2569 เวลา 08.00 น. ร่วมงานสถาปนา", now=datetime(2026,8,31,12,0))
assert p.event_time.isoformat(timespec='minutes') == '2026-09-01T08:00'
assert p.remind_time.isoformat(timespec='minutes') == '2026-09-01T07:30'
print("Parser self-test: PASS")
PY

touch "$APP_DIR/INSTALL_COMPLETE"
chown "$TARGET_USER:$TARGET_GROUP" "$APP_DIR/INSTALL_COMPLETE"

echo
echo "============================================================"
echo " INSTALL COMPLETE"
echo "============================================================"
echo "ทดสอบอุปกรณ์เสียง : arty-audio"
echo "เริ่มตั้งเตือนด้วยเสียง: arty-reminder"
echo "ทดสอบเตือน 1 นาที : arty-test"
echo "ดูรายการ            : arty-list"
echo "ดู service           : arty-status"
echo
echo "หมายเหตุ: ถ้าเพิ่งเพิ่ม user เข้า group audio ให้ logout/login หรือ reboot 1 ครั้ง"
