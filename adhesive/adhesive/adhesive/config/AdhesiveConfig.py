import abc
import os
from typing import Any, List


def convert_to_bool(value: Any) -> bool:
    if not value:
        return False

    string_value = str(value)

    if string_value.upper() == "FALSE" or string_value == "0":
        return False

    return True


class AdhesiveConfig:
    def __init__(self):
        pass

    @abc.abstractmethod
    def __getattr__(self, item) -> Any:
        pass

    def secret_locations(self) -> List[str]:
        return [
            os.path.join(".", ".adhesive", "secrets"),
            os.path.join(os.environ.get("HOME", "."), ".adhesive", "secrets"),
        ]

    @property
    def boolean(self) -> 'AdhesiveBooleanResolver':
        return AdhesiveBooleanResolver(self)


class AdhesiveBooleanResolver:
    def __init__(self, config) -> None:
        self._config = config

    def __getattr__(self, key: str) -> bool:
        value = self._config.__getattr__(key)
        return convert_to_bool(value)

