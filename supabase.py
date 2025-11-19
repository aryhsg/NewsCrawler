import sqlite3
import json

DB_NAME = "VB_news.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS articles (
    key_id TEXT PRIMARY KEY,
    category TEXT,
    url TEXT,
    title TEXT,
    content TEXT NOT NULL
    )
    """
)
conn.commit()