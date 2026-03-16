from __future__ import annotations
from pathlib import Path
from alfred.constants import DATA_DIR


class SandboxManager:
    def __init__(self) -> None:
        self.root = DATA_DIR / "sandboxes" / "self_rewrites"
        self.root.mkdir(parents=True, exist_ok=True)

    def create_trial(self, target: str) -> Path:
        path = self.root / target.replace("/", "_")
        path.mkdir(parents=True, exist_ok=True)
        return path
