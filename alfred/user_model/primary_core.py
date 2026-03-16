from __future__ import annotations


class PrimaryCore:
    def __init__(self, memory) -> None:
        self.memory = memory

    def current_primary_state(self) -> dict:
        return {
            "active_missions": self.memory.list_missions(),
            "recent_consultations": self.memory.list_recent_consultations(limit=5),
        }
