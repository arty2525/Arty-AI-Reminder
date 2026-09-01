"""Interactive GPIO test for Arty AI Reminder V2."""
import time

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hardware import HardwareOutputs, make_button


def main():
    outputs = HardwareOutputs(green=True, yellow=True, red=True, buzzer=True)
    try:
        print("ทดสอบ LED เขียว")
        outputs.green.on(); time.sleep(0.7); outputs.green.off()
        print("ทดสอบ LED เหลือง")
        outputs.yellow.on(); time.sleep(0.7); outputs.yellow.off()
        print("ทดสอบ LED แดง + Buzzer")
        outputs.reminder_alert(cycles=2)

        button = make_button()
        print("กดปุ่ม GPIO17 ภายใน 10 วินาที...")
        if button.wait_for_press(timeout=10):
            print("BUTTON: PASS")
        else:
            print("BUTTON: TIMEOUT")
        button.close()
    finally:
        outputs.close()


if __name__ == "__main__":
    main()
