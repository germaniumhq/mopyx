from typing import List, Optional, Any
import copy
import yaml


# FIXME: move this to its own library: YamlDict seems a good name
from yamldict.YamlNavigator import YamlNavigator


class YamlList(YamlNavigator[List[Any]]):
    """
    A property navigator that allows accessing a list and
    correctly wraps potentially nested dictionaries.
    """

    def __init__(self, *, content: Optional[List] = None, property_name: str = ""):
        super(YamlList, self).__init__()

        self.__content = content if content is not None else list()
        self.__property_name = property_name

    def __deepcopy__(self, memodict={}):
        return YamlList(
            property_name=self.__property_name, content=copy.deepcopy(self.__content)
        )

    def __getitem__(self, item):
        result = self.__content[item]

        if isinstance(result, dict):
            return YamlDict(
                property_name=f"{self.__property_name}.{item}", content=result
            )

        if isinstance(result, list):
            return YamlList(
                property_name=f"{self.__property_name}.{item}", content=result
            )

        return result

    def __setitem__(self, key, value):
        if isinstance(value, YamlNavigator):
            value = value._raw

        self.__content[key] = value

    def __delitem__(self, key):
        self.__content.__delitem__(key)

    def __iter__(self):
        return YamlIteratorWrapper(
            iter=self.__content.__iter__(),
            property_name=self.__property_name,
        )

    def __len__(self) -> int:
        return len(self.__content)

    @property
    def _raw(self) -> List:
        """
        Get access to the underlying collection.
        :return:
        """
        return self.__content

    def __repr__(self):
        return f"YamlList({self.__property_name}) {self.__content}"


from yamldict.YamlDictClass import YamlDict
from yamldict.YamlIteratorWrapper import YamlIteratorWrapper


def yaml_representer(dumper, data):
    return dumper.represent_data(data._raw)


yaml.add_representer(YamlList, yaml_representer, Dumper=yaml.SafeDumper)
