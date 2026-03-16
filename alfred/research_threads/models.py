from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ResearchThread:
    thread_id: str
    topic: str
    consultation_type: str
    summary: str = ""
