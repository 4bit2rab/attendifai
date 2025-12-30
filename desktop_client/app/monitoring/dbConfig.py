import sqlite3

DB_PATH = "attendance_agent.db"

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---------------- AUTH TOKEN ----------------
    # Drop old table if schema was incorrect (only for dev, safe to remove in prod)
    cursor.execute("DROP TABLE IF EXISTS auth_token")

    # Create auth_token table with correct default for created_at
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ---------------- DAILY SUMMARY ----------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            date TEXT PRIMARY KEY,
            productive_seconds INTEGER DEFAULT 0,
            idle_seconds INTEGER DEFAULT 0,
            overtime_seconds INTEGER DEFAULT 0,
            synced INTEGER DEFAULT 0
        )
    """)

    # ---------------- OPTIONAL: ACTIVITY LOG ----------------
    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS activity_log (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         log_date TEXT NOT NULL,
    #         productive_seconds INTEGER DEFAULT 0,
    #         idle_seconds INTEGER DEFAULT 0,
    #         overtime_seconds INTEGER DEFAULT 0,
    #         synced INTEGER DEFAULT 0
    #     )
    # """)

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

def add_session(session_type, start_time, end_time):
        # start_time, end_time = clip_session_to_shift(start_time, end_time)
        # if start_time is None:
        #     return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO employee_activity (date, start_time, end_time, type,synced,overtime)
            VALUES (?, ?, ?, ?,?,?)""",
            (str(start_time.date()), start_time, end_time, session_type, 0, 0),
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

 
