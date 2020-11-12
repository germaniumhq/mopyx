from typing import Any

from adhesive.config.AdhesiveConfig import AdhesiveConfig


class NoopAdhesiveConfig(AdhesiveConfig):
    def __getattr__(self, item: str) -> Any:
        return None
