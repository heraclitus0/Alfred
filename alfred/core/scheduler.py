from __future__ import annotations
import time
from dataclasses import dataclass
from alfred.types import Event


@dataclass
class Job:
    name: str
    run_at: float
    event_name: str
    payload: dict


class Scheduler:
    def __init__(self, event_bus) -> None:
        self.event_bus = event_bus
        self.jobs: list[Job] = []

    def schedule_in(self, seconds: int, event_name: str, payload: dict, name: str | None = None) -> None:
        self.jobs.append(Job(name or event_name, time.time() + seconds, event_name, payload))

    def run_once_due_jobs(self) -> None:
        now = time.time()
        due = [j for j in self.jobs if j.run_at <= now]
        self.jobs = [j for j in self.jobs if j.run_at > now]
        for job in due:
            self.event_bus.publish(Event(job.event_name, job.payload))
