import subprocess
from pathlib import Path
from config import WHISPER_BIN, WHISPER_MODEL


def transcribe(wav_path: Path) -> str:
    if not WHISPER_BIN.exists():
        raise FileNotFoundError(f"ไม่พบโปรแกรม Whisper: {WHISPER_BIN}")
    if not WHISPER_MODEL.exists():
        raise FileNotFoundError(f"ไม่พบโมเดล Whisper: {WHISPER_MODEL}")

    output_base = wav_path.with_suffix("")
    output_txt = Path(str(output_base) + ".txt")
    if output_txt.exists():
        output_txt.unlink()

    command = [
        str(WHISPER_BIN),
        "-m", str(WHISPER_MODEL),
        "-f", str(wav_path),
        "-l", "th",
        "-t", "4",
        "-nt",
        "-otxt",
        "-of", str(output_base),
    ]
    subprocess.run(command, check=True)

    if not output_txt.exists():
        raise RuntimeError("Whisper ไม่ได้สร้างไฟล์ข้อความ")
    return output_txt.read_text(encoding="utf-8").strip()
