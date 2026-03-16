from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import time

class Mode(str, Enum):
    OFF = "OFF"
    PASSIVE = "PASSIVE"
    MONITORING = "MONITORING"
    ACTIVE = "ACTIVE"
    HALT = "HALT"


class ConsultationType(str, Enum):
    SELF_IMPROVEMENT = "self_improvement"
    WORLD_AWARENESS = "world_awareness"
    INTERACTION_REFINEMENT = "interaction_refinement"
    MISSION_STRATEGY = "mission_strategy"


@dataclass
class Event:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    ts: float = field(default_factory=time.time)


@dataclass
class RuntimeStatus:
    mode: Mode
    started_at: float
    loops_running: list[str]
    last_checkpoint: float | None = None
