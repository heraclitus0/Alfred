from __future__ import annotations
import time


class KillSwitch:
    def __init__(self, memory) -> None:
        self.memory = memory
        self.triggered = False
        self.reason = None

    def trigger(self, reason: str) -> None:
        self.triggered = True
        self.reason = reason
        self.memory.put("safety", "kill_switch", {"reason": reason, "ts": time.time()})
