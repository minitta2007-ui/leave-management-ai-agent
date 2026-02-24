import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY,
    student_id TEXT,
    days INTEGER,
    current_stage TEXT,
    final_status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS approval_logs (
    leave_id INTEGER,
    role TEXT,
    decision TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database tables created successfully!")