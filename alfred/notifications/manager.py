from __future__ import annotations


class NotificationManager:
    def __init__(self, memory) -> None:
        self.memory = memory
        self.buffer = []

    def emit(self, payload: dict | object) -> None:
        self.buffer.append(payload)
        self.memory.put("notifications", "latest", payload if isinstance(payload, dict) else getattr(payload, "__dict__", {"value": str(payload)}))
