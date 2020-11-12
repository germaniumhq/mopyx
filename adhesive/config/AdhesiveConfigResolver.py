from typing import Any

from adhesive.config.AdhesiveConfig import AdhesiveConfig


class AdhesiveConfigResolver:
    """
    This only holds the wrapper over getattr to allow
    fetching settings directly.
    """
    def __init__(self, adhesive_config: AdhesiveConfig):
        self.config = adhesive_config

    def __getattr__(self, item: str) -> Any:
        return getattr(self.config, item)
