from __future__ import annotations
import time
from alfred.types import Mode


class StateManager:
    def __init__(self) -> None:
        self.mode: Mode = Mode.OFF
        self.last_checkpoint: float | None = None
        self.meta: dict[str, object] = {}

    def set_mode(self, mode: Mode) -> None:
        self.mode = mode
        self.meta["mode_changed_at"] = time.time()

    def snapshot(self) -> dict:
        return {"mode": self.mode.value, "last_checkpoint": self.last_checkpoint, "meta": self.meta}

    def restore(self, data: dict) -> None:
        self.mode = Mode(data.get("mode", Mode.OFF.value))
        self.last_checkpoint = data.get("last_checkpoint")
        self.meta = data.get("meta", {})
