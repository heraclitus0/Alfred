from __future__ import annotations
from dataclasses import dataclass
from alfred import __version__


@dataclass
class VersionStamp:
    version: str

    @classmethod
    def current(cls) -> "VersionStamp":
        return cls(version=__version__)
