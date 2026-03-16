from __future__ import annotations
from uuid import uuid4
from alfred.missions.models import Mission


class MissionManager:
    def __init__(self, memory) -> None:
        self.memory = memory

    def create(self, name: str, **kwargs) -> Mission:
        mission = Mission(mission_id=str(uuid4()), name=name, **kwargs)
        self.memory.save_mission(mission)
        return mission
