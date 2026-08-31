import subprocess
from pathlib import Path
from config import AUDIO_DIR, RECORD_SECONDS


def record_wav(filename="command.wav", seconds=RECORD_SECONDS) -> Path:
    wav_path = AUDIO_DIR / filename
    command = [
        "arecord",
        "-f", "S16_LE",
        "-r", "16000",
        "-c", "1",
        "-d", str(seconds),
        str(wav_path),
    ]
    print(f"กำลังบันทึกเสียง {seconds} วินาที...")
    subprocess.run(command, check=True)
    return wav_path
