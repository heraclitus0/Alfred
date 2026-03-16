from __future__ import annotations
from shutil import disk_usage
from alfred.watchers.signal_models import Signal


class StorageWatcher:
    name = "storage"
    def tick(self):
        total, used, free = disk_usage(".")
        pct = used / total
        if pct >= 0.9:
            return [Signal(kind="device.storage", message=f"Disk usage high: {pct:.0%}", score=0.92)]
        return []
