import os
from typing import Any, Dict

from adhesive.config.AdhesiveConfig import AdhesiveConfig


class LocalAdhesiveConfig(AdhesiveConfig):
    """
    A configuration that's assembled from the local files.
    """
    def __init__(self,
                 user_config: Dict[str, Any],
                 local_config: Dict[str, Any],
                 environment: Dict[str, str]):
        super(LocalAdhesiveConfig, self).__init__()

        # FIXME: detect if possible where's the /tmp folder
        self._defaults = {
            "color": True,
            "stdout": False,
            "temp_folder": "/tmp/adhesive",
            "log_level": "info",
            "plugins": [],
        }

        self._program_config: Dict[str, Any] = dict()
        self._local_config = local_config if local_config is not None else dict()
        self._user_config = user_config if user_config is not None else dict()
        self._environment = environment if environment is not None else os.environ

    def __getattr__(self, item: str) -> Any:
        if item in self._program_config:
            return self._program_config[item]

        env_name = f"ADHESIVE_{item.upper()}"

        if env_name in self._environment:
            if env_name.endswith("_LIST"):
                return self._environment[env_name].split(os.path.pathsep)
            return self._environment[env_name]

        if item in self._local_config:
            return self._local_config[item]

        if item in self._user_config:
            return self._user_config[item]

        if item in self._defaults:
            return self._defaults[item]

        return None

    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith("_"):
            super(LocalAdhesiveConfig, self).__setattr__(key, value)
            return

        self._program_config[key] = value
