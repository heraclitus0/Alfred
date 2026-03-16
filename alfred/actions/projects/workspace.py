from __future__ import annotations
from pathlib import Path
from alfred.constants import DATA_DIR


class WorkspaceManager:
    def __init__(self) -> None:
        self.root = DATA_DIR / "sandboxes" / "code"
        self.root.mkdir(parents=True, exist_ok=True)

    def create_workspace(self, name: str) -> Path:
        path = self.root / name
        path.mkdir(parents=True, exist_ok=True)
        return path
