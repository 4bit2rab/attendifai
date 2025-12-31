import sqlite3

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

 
