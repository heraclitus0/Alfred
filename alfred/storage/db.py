from __future__ import annotations
import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv


class Database:
    def __init__(self) -> None:
        load_dotenv()
        path = os.getenv("ALFRED_DB_PATH", "data/runtime/alfred.db")
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def init(self) -> None:
        with self.connect() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS missions (
                    mission_id TEXT PRIMARY KEY,
                    name TEXT,
                    payload TEXT,
                    created_at REAL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    store TEXT,
                    key TEXT,
                    value TEXT,
                    created_at REAL DEFAULT (strftime('%s','now'))
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS research_threads (
                    thread_id TEXT PRIMARY KEY,
                    topic TEXT,
                    consultation_type TEXT,
                    summary TEXT,
                    updated_at REAL DEFAULT (strftime('%s','now'))
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS consultations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT,
                    consultation_type TEXT,
                    topic TEXT,
                    prompt TEXT,
                    response TEXT,
                    created_at REAL DEFAULT (strftime('%s','now'))
                )
            """)
