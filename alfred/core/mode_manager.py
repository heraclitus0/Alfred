from __future__ import annotations
from alfred.types import Mode
from alfred.exceptions import InvalidModeTransition


_ALLOWED = {
    Mode.OFF: {Mode.PASSIVE},
    Mode.PASSIVE: {Mode.MONITORING, Mode.ACTIVE, Mode.HALT, Mode.OFF},
    Mode.MONITORING: {Mode.PASSIVE, Mode.ACTIVE, Mode.HALT},
    Mode.ACTIVE: {Mode.PASSIVE, Mode.MONITORING, Mode.HALT},
    Mode.HALT: {Mode.OFF},
}


class ModeManager:
    def __init__(self, state):
        self.state = state

    def set_mode(self, mode: Mode) -> None:
        current = self.state.mode
        if current != mode and mode not in _ALLOWED.get(current, set()):
            raise InvalidModeTransition(f"Cannot transition {current} -> {mode}")
        self.state.set_mode(mode)
