from enum import Enum


class CheckState(Enum):
    Checked: int = 0
    Unchecked: int = 1
    PartiallyChecked: int = 2


ItemIsUserCheckable = 1

