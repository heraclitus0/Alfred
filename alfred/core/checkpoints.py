from __future__ import annotations
import json
import time
from pathlib import Path
from alfred.constants import CHECKPOINT_DIR


class CheckpointManager:
    def __init__(self, state) -> None:
        self.state = state
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
        self.path = CHECKPOINT_DIR / "runtime.json"

    def save(self) -> None:
        self.state.last_checkpoint = time.time()
        self.path.write_text(json.dumps(self.state.snapshot(), indent=2))

    def restore(self) -> None:
        if self.path.exists():
            self.state.restore(json.loads(self.path.read_text()))
