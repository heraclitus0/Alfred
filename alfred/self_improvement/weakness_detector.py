from __future__ import annotations


class WeaknessDetector:
    def __init__(self, diagnostics) -> None:
        self.diagnostics = diagnostics

    def detect(self, target: str) -> dict:
        base = self.diagnostics.inspect_target(target)
        return {
            "target": target,
            "weakness": f"Observed weakness in {target}: outputs are not yet as concrete and nuanced as desired.",
            "evidence": base,
        }
