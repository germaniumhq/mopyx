from typing import Tuple
from pathlib import Path
import yaml
import os

from germanium_build_monitor.model import RootModel
from germanium_build_monitor.model import Settings

user_home = str(Path.home())


def persist_state(root: RootModel.RootModel,
                  settings: Settings.Settings) -> None:
    with open(os.path.join(user_home, ".felixbm"), "w", encoding="utf-8") as f:
        yaml.dump([
            root.as_dict(),
            settings.as_dict(),
        ], f)


def load_state() -> Tuple[RootModel.RootModel, Settings.Settings]:
    persisted_state_file = os.path.join(user_home, ".felixbm")
    if not os.path.exists(persisted_state_file):
        return RootModel.RootModel(), Settings.Settings()

    with open(persisted_state_file, "r", encoding="utf-8") as f:
        items = list(yaml.safe_load(f))

        return RootModel.RootModel.from_dict(items[0]), \
            Settings.Settings.from_dict(items[1])
