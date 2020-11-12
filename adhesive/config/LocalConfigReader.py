from typing import Dict, Any
import os

from adhesive.config.LocalAdhesiveConfig import LocalAdhesiveConfig
import yaml


def read_configuration(cwd=".",
                       environment=os.environ) -> LocalAdhesiveConfig:
    user_config_path = os.path.join(
        environment.get("HOME", ""),
        ".adhesive", "config.yml"
    )
    user_config = read_configuration_from_file(user_config_path)

    local_config_path = os.path.join(cwd, ".adhesive", "config.yml")
    local_config = read_configuration_from_file(local_config_path)

    return LocalAdhesiveConfig(
        user_config=user_config,
        local_config=local_config,
        environment=environment,
    )


def read_configuration_from_file(path: str) -> Dict[str, Any]:
    try:
        with open(path, "rt") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(e)
        return dict()
