"""GPIO helpers for Arty AI Reminder V2.

BCM pin map:
- Button: GPIO17 (to GND, internal pull-up)
- Green LED: GPIO27
- Yellow LED: GPIO22
- Red LED: GPIO23
- Active buzzer signal: GPIO24

The module gracefully falls back to no-op devices when GPIO is unavailable,
so parser/unit tests can still run on non-Raspberry Pi machines.
"""
from contextlib import suppress
import time

BUTTON_PIN = 17
LED_GREEN_PIN = 27
LED_YELLOW_PIN = 22
LED_RED_PIN = 23
BUZZER_PIN = 24

try:
    from gpiozero import Button, LED, Buzzer
    GPIO_AVAILABLE = True
except Exception:
    Button = LED = Buzzer = None
    GPIO_AVAILABLE = False


class NullOutput:
    def on(self):
        pass

    def off(self):
        pass

    def blink(self, *args, **kwargs):
        pass

    def beep(self, *args, **kwargs):
        pass

    def close(self):
        pass


class HardwareOutputs:
    """Own a selected set of output pins without claiming unrelated pins."""

    def __init__(self, green=False, yellow=False, red=False, buzzer=False):
        self.green = self._led(LED_GREEN_PIN) if green else NullOutput()
        self.yellow = self._led(LED_YELLOW_PIN) if yellow else NullOutput()
        self.red = self._led(LED_RED_PIN) if red else NullOutput()
        self.buzzer = self._buzzer(BUZZER_PIN) if buzzer else NullOutput()

    @staticmethod
    def _led(pin):
        if not GPIO_AVAILABLE:
            return NullOutput()
        try:
            return LED(pin)
        except Exception as exc:
            print(f"[GPIO] LED GPIO{pin} unavailable: {exc}")
            return NullOutput()

    @staticmethod
    def _buzzer(pin):
        if not GPIO_AVAILABLE:
            return NullOutput()
        try:
            return Buzzer(pin)
        except Exception as exc:
            print(f"[GPIO] Buzzer GPIO{pin} unavailable: {exc}")
            return NullOutput()

    def all_off(self):
        for dev in (self.green, self.yellow, self.red, self.buzzer):
            with suppress(Exception):
                dev.off()

    def reminder_alert(self, cycles=3):
        for _ in range(cycles):
            self.red.on()
            self.buzzer.on()
            time.sleep(0.25)
            self.red.off()
            self.buzzer.off()
            time.sleep(0.20)

    def close(self):
        self.all_off()
        for dev in (self.green, self.yellow, self.red, self.buzzer):
            with suppress(Exception):
                dev.close()


def make_button():
    if not GPIO_AVAILABLE:
        raise RuntimeError("gpiozero ไม่พร้อมใช้งานบนเครื่องนี้")
    # Button connects GPIO17 to GND. pull_up=True uses the Pi internal pull-up.
    return Button(BUTTON_PIN, pull_up=True, bounce_time=0.08)
