"""Push-button service for Arty AI Reminder V2.

Idle: green LED ON.
Press GPIO17 button: green OFF, yellow ON, run one voice-reminder cycle.
When finished: yellow OFF, green ON.
"""
import signal
import subprocess
import sys
import time
from pathlib import Path

from hardware import HardwareOutputs, make_button

APP_DIR = Path("/opt/arty-ai-reminder")
VOICE_APP = APP_DIR / "voice_assistant.py"

running = True
busy = False


def stop_service(*_args):
    global running
    running = False


def main():
    global busy
    signal.signal(signal.SIGTERM, stop_service)
    signal.signal(signal.SIGINT, stop_service)

    outputs = HardwareOutputs(green=True, yellow=True)
    button = make_button()
    outputs.green.on()
    print("Arty push-button daemon started: GPIO17")

    def on_press():
        global busy
        if busy:
            return
        busy = True
        outputs.green.off()
        outputs.yellow.on()
        try:
            subprocess.run(
                [sys.executable, str(VOICE_APP), "--once"],
                cwd=str(APP_DIR),
                check=False,
            )
        finally:
            outputs.yellow.off()
            outputs.green.on()
            busy = False

    button.when_pressed = on_press

    try:
        while running:
            time.sleep(0.25)
    finally:
        outputs.close()
        button.close()


if __name__ == "__main__":
    main()
