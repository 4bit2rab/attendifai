import sqlite3
from datetime import datetime

conn = sqlite3.connect("activity.db", check_same_thread=False)
cursor = conn.cursor()

# ========================
# TABLES
# ========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    active_seconds INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS overtime_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    overtime_seconds INTEGER,
    approved INTEGER
)
""")

conn.commit()

# ========================
# FUNCTIONS
# ========================

def save_minute_activity(active_seconds: int):
    timestamp = datetime.now().isoformat(timespec="seconds")
    cursor.execute(
        "INSERT INTO activity_log (timestamp, active_seconds) VALUES (?, ?)",
        (timestamp, active_seconds)
    )
    conn.commit()


def save_overtime(overtime_seconds: int, approved: bool):
    date = datetime.now().date().isoformat()
    cursor.execute(
        "INSERT INTO overtime_log (date, overtime_seconds, approved) VALUES (?, ?, ?)",
        (date, overtime_seconds, int(approved))
    )
    conn.commit()


# ========================
# GETTER FUNCTIONS FOR API
# ========================

def get_minute_activity_logs():
    cursor.execute("SELECT id, timestamp, active_seconds FROM activity_log ORDER BY id DESC")
    rows = cursor.fetchall()
    logs = [
        {"id": row[0], "timestamp": row[1], "seconds": row[2]}
        for row in rows
    ]
    return logs


def get_overtime_logs():
    cursor.execute("SELECT id, date, overtime_seconds, approved FROM overtime_log ORDER BY id DESC")
    rows = cursor.fetchall()
    logs = [
        {"id": row[0], "minutes": row[2] // 60, "approved": bool(row[3]), "timestamp": row[1]}
        for row in rows
    ]
    return logs
