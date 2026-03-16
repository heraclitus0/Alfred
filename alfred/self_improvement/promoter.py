from __future__ import annotations
import time


class PromotionManager:
    def __init__(self, memory) -> None:
        self.memory = memory

    def promote(self, result: dict) -> None:
        self.memory.put("promotions", result["target"], {"promoted_at": time.time(), "result": result})
