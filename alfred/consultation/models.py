from __future__ import annotations
from dataclasses import dataclass, field
import time


@dataclass
class ConsultationRecord:
    thread_id: str
    consultation_type: str
    topic: str
    prompt: str
    response: str
    created_at: float = field(default_factory=time.time)
