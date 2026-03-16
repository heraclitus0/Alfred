from __future__ import annotations
from alfred.autonomy.authority import ALLOWED_SAFE_REWRITE_TARGETS
from alfred.exceptions import ApprovalRequired


class ApprovalEngine:
    def approve_rewrite_target(self, target: str) -> bool:
        return target in ALLOWED_SAFE_REWRITE_TARGETS

    def ensure_rewrite_target_allowed(self, target: str) -> None:
        if not self.approve_rewrite_target(target):
            raise ApprovalRequired(f"Rewrite target requires explicit approval: {target}")
