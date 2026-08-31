import sqlite3
from datetime import datetime
from config import DB_PATH


def connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    with connect() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                event_time TEXT NOT NULL,
                remind_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL
            )
            """
        )
        con.commit()


def add_reminder(event, event_time, remind_time):
    created_at = datetime.now().isoformat(timespec="seconds")
    with connect() as con:
        cur = con.execute(
            """
            INSERT INTO reminders(event, event_time, remind_time, status, created_at)
            VALUES (?, ?, ?, 'pending', ?)
            """,
            (
                event,
                event_time.isoformat(timespec="seconds"),
                remind_time.isoformat(timespec="seconds"),
                created_at,
            ),
        )
        con.commit()
        return cur.lastrowid


def get_due_reminders(now=None):
    now = now or datetime.now()
    with connect() as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            """
            SELECT * FROM reminders
            WHERE status = 'pending' AND remind_time <= ? AND event_time >= ?
            ORDER BY remind_time ASC
            """,
            (now.isoformat(timespec="seconds"), now.isoformat(timespec="seconds")),
        ).fetchall()
    return rows


def mark_missed_before(now=None):
    now = now or datetime.now()
    with connect() as con:
        con.execute(
            """
            UPDATE reminders
            SET status = 'missed'
            WHERE status = 'pending' AND event_time < ?
            """,
            (now.isoformat(timespec="seconds"),),
        )
        con.commit()


def mark_notified(reminder_id):
    with connect() as con:
        con.execute(
            "UPDATE reminders SET status = 'notified' WHERE id = ?",
            (reminder_id,),
        )
        con.commit()


def list_reminders(limit=20):
    with connect() as con:
        con.row_factory = sqlite3.Row
        return con.execute(
            """
            SELECT * FROM reminders
            ORDER BY event_time ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
