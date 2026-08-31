import shutil
import subprocess


def speak(text: str):
    if not shutil.which("espeak-ng"):
        print("[TTS]", text)
        return
    subprocess.run(
        ["espeak-ng", "-v", "th", "-s", "145", text],
        check=False,
    )
