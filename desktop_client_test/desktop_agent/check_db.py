import sqlite3

conn = sqlite3.connect("activity.db")
cursor = conn.cursor()

rows = cursor.execute("SELECT * FROM activity_log").fetchall()

for row in rows:
    print(row)
