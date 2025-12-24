import sqlite3

DB_PATH = "attendance_agent.db"

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employee_activity(
        id INTEGER PRIMARY KEY AUTOINCREMENT,        
        date TEXT NOT NULL,
        start_time TIMESTAMP NOT NULL,              
        end_time TIMESTAMP NOT NULL,        
        type TEXT CHECK(type IN ('productive', 'idle')) NOT NULL,
        synced INT NOT NULL
        overtime INT NOT NULL
        )    
        """
    )
    cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS auth_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()