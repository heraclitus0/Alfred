from __future__ import annotations
from alfred.watchers.device.storage import StorageWatcher


class WatcherManager:
    def __init__(self, memory, notifications) -> None:
        self.memory = memory
        self.notifications = notifications
        self.watchers = [StorageWatcher()]

    def tick(self) -> None:
        for watcher in self.watchers:
            signals = watcher.tick()
            for signal in signals:
                self.notifications.emit(signal)
