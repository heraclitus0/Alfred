from __future__ import annotations
from dataclasses import dataclass, field
import time


@dataclass
class Mission:
    mission_id: str
    name: str
    importance: float = 0.5
    urgency: float = 0.5
    volatility: float = 0.5
    state: str = "active"
    created_at: float = field(default_factory=time.time)
