from __future__ import annotations
import json
from dataclasses import asdict, is_dataclass


class MemoryFacade:
    def __init__(self, db) -> None:
        self.db = db

    def _dump(self, value) -> str:
        if is_dataclass(value):
            return json.dumps(asdict(value))
        return json.dumps(value)

    def save_mission(self, mission) -> None:
        with self.db.connect() as con:
            con.execute(
                "INSERT OR REPLACE INTO missions (mission_id, name, payload, created_at) VALUES (?, ?, ?, ?)",
                (mission.mission_id, mission.name, self._dump(mission), mission.created_at),
            )

    def list_missions(self):
        with self.db.connect() as con:
            rows = con.execute("SELECT mission_id, name, payload FROM missions ORDER BY created_at DESC").fetchall()
        return [json.loads(r[2]) for r in rows]

    def put(self, store: str, key: str, value) -> None:
        with self.db.connect() as con:
            con.execute("INSERT INTO memory_entries (store, key, value) VALUES (?, ?, ?)", (store, key, self._dump(value)))

    def get_latest(self, store: str, key: str):
        with self.db.connect() as con:
            row = con.execute(
                "SELECT value FROM memory_entries WHERE store=? AND key=? ORDER BY id DESC LIMIT 1",
                (store, key),
            ).fetchone()
        return json.loads(row[0]) if row else None

    def list_recent(self, store: str, limit: int = 10):
        with self.db.connect() as con:
            rows = con.execute(
                "SELECT key, value FROM memory_entries WHERE store=? ORDER BY id DESC LIMIT ?",
                (store, limit),
            ).fetchall()
        return [{"key": r[0], "value": json.loads(r[1])} for r in rows]

    def save_thread(self, thread_id: str, topic: str, consultation_type: str, summary: str) -> None:
        with self.db.connect() as con:
            con.execute(
                "INSERT OR REPLACE INTO research_threads (thread_id, topic, consultation_type, summary, updated_at) VALUES (?, ?, ?, ?, strftime('%s','now'))",
                (thread_id, topic, consultation_type, summary),
            )

    def get_thread(self, thread_id: str):
        with self.db.connect() as con:
            row = con.execute(
                "SELECT thread_id, topic, consultation_type, summary FROM research_threads WHERE thread_id=?",
                (thread_id,),
            ).fetchone()
        if not row:
            return None
        return {"thread_id": row[0], "topic": row[1], "consultation_type": row[2], "summary": row[3]}

    def find_thread(self, topic: str, consultation_type: str):
        with self.db.connect() as con:
            row = con.execute(
                "SELECT thread_id, topic, consultation_type, summary FROM research_threads WHERE topic=? AND consultation_type=? ORDER BY updated_at DESC LIMIT 1",
                (topic, consultation_type),
            ).fetchone()
        if not row:
            return None
        return {"thread_id": row[0], "topic": row[1], "consultation_type": row[2], "summary": row[3]}

    def save_consultation(self, thread_id: str, consultation_type: str, topic: str, prompt: str, response: str) -> None:
        with self.db.connect() as con:
            con.execute(
                "INSERT INTO consultations (thread_id, consultation_type, topic, prompt, response) VALUES (?, ?, ?, ?, ?)",
                (thread_id, consultation_type, topic, prompt, response),
            )

    def list_thread_consultations(self, thread_id: str, limit: int = 20):
        with self.db.connect() as con:
            rows = con.execute(
                "SELECT prompt, response, created_at FROM consultations WHERE thread_id=? ORDER BY id ASC LIMIT ?",
                (thread_id, limit),
            ).fetchall()
        return [{"prompt": r[0], "response": r[1], "created_at": r[2]} for r in rows]

    def list_recent_consultations(self, limit: int = 10):
        with self.db.connect() as con:
            rows = con.execute(
                "SELECT consultation_type, topic, response FROM consultations ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [{"consultation_type": r[0], "topic": r[1], "response": r[2]} for r in rows]
