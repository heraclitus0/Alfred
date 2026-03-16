from dataclasses import dataclass

@dataclass
class Signal:
    kind: str
    message: str
    score: float = 0.5
