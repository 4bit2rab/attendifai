import sqlite3
from datetime import date, datetime

DB_PATH = "attendance_agent.db"

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create auth_token table with correct default for created_at
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employee_activity(
        id INTEGER PRIMARY KEY AUTOINCREMENT,        
        date TEXT NOT NULL,
        start_time TIMESTAMP NOT NULL,              
        end_time TIMESTAMP NOT NULL,        
        type TEXT CHECK(type IN ('productive', 'idle')) NOT NULL,
        synced INT NOT NULL,
        overtime INT NOT NULL
        )    
        """
    )
    
    conn.commit()
    conn.close()

def add_session(session_type, start_time, end_time,overtime=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO employee_activity (date, start_time, end_time, type,synced,overtime)
        VALUES (?, ?, ?, ?,?,?)""",
        (str(start_time.date()), start_time, end_time, session_type, 0, overtime),
    )
    conn.commit()
    conn.close()

def is_employee_registered() -> bool:
    """Check if auth_token table has any entry"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM auth_token")
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_daily_productivity(target_date: date):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT type, start_time, end_time
        FROM employee_activity
        WHERE date = ? AND synced = 0 AND overtime = 0
    """,
        (target_date.isoformat(),),
    )

    productive_seconds = 0
    idle_seconds = 0

    for session_type, start, end in cursor.fetchall():
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        duration = max(0, int((end_dt - start_dt).total_seconds()))

        if session_type == "productive":
            productive_seconds += duration
        else:
            idle_seconds += duration

    cursor.execute(
        """
        SELECT start_time, end_time
        FROM employee_activity
        WHERE date = ?
        AND synced = 0
        AND overtime = 1
        AND type = 'productive'
        """,
        (target_date.isoformat(),),
    )
    overtime_productive_seconds = 0

    for start, end in cursor.fetchall():
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        overtime_productive_seconds += max(
            0, int((end_dt - start_dt).total_seconds())
        )

    conn.close()

    return productive_seconds, idle_seconds, overtime_productive_seconds

def mark_day_as_synced(date_str: date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE employee_activity
        SET synced = 1
        WHERE date = ?
    """,
        (date_str.isoformat(),),
    )

    conn.commit()
    conn.close()
