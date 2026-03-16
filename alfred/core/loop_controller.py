from __future__ import annotations
from typing import Callable


class LoopController:
    def __init__(self, event_bus) -> None:
        self.event_bus = event_bus
        self._loops: dict[str, Callable[[], None]] = {}
        self._running: set[str] = set()

    def start(self, name: str, tick: Callable[[], None]) -> None:
        self._loops[name] = tick
        self._running.add(name)

    def stop(self, name: str) -> None:
        self._running.discard(name)

    def stop_all(self) -> None:
        self._running.clear()

    def run_once(self) -> None:
        for name in list(self._running):
            self._loops[name]()

    def running_loops(self) -> list[str]:
        return sorted(self._running)
