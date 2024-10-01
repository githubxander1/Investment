# utils/database.py
import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT,
                    date TEXT,
                    reminder_time TEXT,
                    repeat TEXT,
                    tags TEXT
                )''')
    conn.commit()
    conn.close()

create_database()