from typing import Dict, Union, List
from mypy_extensions import TypedDict


ImagesDict = Dict[str, Union[str, List[str]]]


class ConfigDictRequired(TypedDict):
    images: ImagesDict


class ConfigDict(ConfigDictRequired, total=False):
    push: bool


Config = Union[ImagesDict, ConfigDict]
