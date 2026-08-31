#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $EUID -ne 0 ]]; then
  echo "กรุณารัน: sudo ./update.sh"
  exit 1
fi
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_USER="${SUDO_USER:-${USER:-ubuntu}}"
TARGET_GROUP="$(id -gn "$TARGET_USER")"
install -m 0644 "$REPO_DIR"/src/*.py /opt/arty-ai-reminder/
chown -R "$TARGET_USER:$TARGET_GROUP" /opt/arty-ai-reminder
python3 -m py_compile /opt/arty-ai-reminder/*.py
systemctl restart arty-ai-reminder.service
echo "Update complete"
