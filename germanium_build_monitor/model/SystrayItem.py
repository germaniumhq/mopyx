from typing import Callable
from mopyx import model

from .BuildStatus import BuildStatus


@model
class SystrayItem:
    def __init__(self,
                 key: str,
                 status: BuildStatus,
                 text: str,
                 action: Callable) -> None:
        self.key = key
        self.text = text
        self.status = status
        self.action = action

