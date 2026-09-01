#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "กรุณารันด้วย sudo"
  exit 1
fi

MODEL="$(tr -d '\0' </proc/device-tree/model 2>/dev/null || true)"
echo "Detected model: ${MODEL:-unknown}"

if [[ "$MODEL" == *"Raspberry Pi 5"* ]]; then
  echo "Raspberry Pi 5 detected — installing gpiozero >= 2.0.1.post3"
  apt-get update
  apt-get install -y python3-pip python3-dev swig liblgpio-dev python3-lgpio
  python3 -m pip install --break-system-packages --upgrade 'gpiozero>=2.0.1.post3'
  python3 - <<'PY'
import gpiozero
print('gpiozero:', gpiozero.__version__)
PY
else
  echo "ไม่ใช่ Raspberry Pi 5 — ไม่ต้องใช้ compatibility fix นี้"
fi
