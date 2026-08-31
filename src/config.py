from pathlib import Path

BASE_DIR = Path('/opt/arty-ai-reminder')
DB_PATH = BASE_DIR / 'reminders.db'
AUDIO_DIR = BASE_DIR / 'audio'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

WHISPER_DIR = Path('/opt/whisper.cpp')
WHISPER_BIN = WHISPER_DIR / 'build' / 'bin' / 'whisper-cli'
WHISPER_MODEL = WHISPER_DIR / 'models' / 'ggml-base.bin'

RECORD_SECONDS = 8
REMIND_BEFORE_MINUTES = 30
CHECK_INTERVAL_SECONDS = 5
