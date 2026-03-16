from __future__ import annotations
from pathlib import Path


class SelfRewriteSandbox:
    def __init__(self, sandbox_manager) -> None:
        self.sandbox_manager = sandbox_manager

    def run(self, proposal: dict) -> dict:
        target = proposal["target"]
        path = self.sandbox_manager.create_trial(target)
        candidate = path / "candidate_patch.txt"
        candidate.write_text(proposal["response"], encoding="utf-8")
        validated = len(proposal["response"].strip()) > 20
        return {
            "target": target,
            "sandbox_path": str(path),
            "candidate_path": str(candidate),
            "validated": validated,
            "proposal": proposal,
        }
