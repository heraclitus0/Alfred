from __future__ import annotations


class DiagnosticsEngine:
    def __init__(self, memory) -> None:
        self.memory = memory

    def inspect_target(self, target: str) -> dict:
        recent = self.memory.list_recent("consultation_learning", limit=5)
        return {
            "target": target,
            "symptoms": ["needs better specificity", "needs more concrete next steps"],
            "recent_context": recent,
        }
