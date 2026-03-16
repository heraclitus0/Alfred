from __future__ import annotations
import time


class HealthMonitor:
    def __init__(self, registry) -> None:
        self.registry = registry
        self.last_tick = None

    def tick(self) -> None:
        self.last_tick = time.time()
