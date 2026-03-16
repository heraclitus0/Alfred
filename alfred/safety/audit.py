from __future__ import annotations
import time


class AuditLogger:
    def __init__(self, memory) -> None:
        self.memory = memory

    def record(self, kind: str, payload: dict) -> None:
        self.memory.put("audit", kind, {"ts": time.time(), **payload})
