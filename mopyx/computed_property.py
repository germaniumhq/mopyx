from typing import TypeVar

T = TypeVar("T")


class ComputedProperty:
    def __init__(self):
        self.initial_render = True
        self.value = None
