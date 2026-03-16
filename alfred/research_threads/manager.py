from __future__ import annotations
from uuid import uuid4


class ResearchThreadManager:
    def __init__(self, memory) -> None:
        self.memory = memory

    def get_or_create(self, topic: str, consultation_type: str) -> dict:
        existing = self.memory.find_thread(topic, consultation_type)
        if existing:
            return existing
        thread_id = str(uuid4())
        self.memory.save_thread(thread_id, topic, consultation_type, summary="")
        return {"thread_id": thread_id, "topic": topic, "consultation_type": consultation_type, "summary": ""}

    def update_summary(self, thread_id: str, topic: str, consultation_type: str, summary: str) -> None:
        self.memory.save_thread(thread_id, topic, consultation_type, summary)
