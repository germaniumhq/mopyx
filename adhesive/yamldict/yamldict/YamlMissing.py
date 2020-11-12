from typing import Any, Union, List, Dict, Optional

from yamldict.YamlNavigator import YamlNavigator


class YamlMissing(YamlNavigator[None]):
    EMPTY_LIST: List[str] = list()

    def __init__(
        self,
        *args,
        parent_property: Optional[Union["YamlDict", "YamlMissing"]],
        property_name: str,
        full_property_name: str,
    ):
        if args:
            raise Exception("You need to pass named arguments")

        if property_name.endswith("__parent_property"):
            raise Exception("Problem")

        super(YamlMissing, self).__init__()

        self.__property_name = property_name
        self.__full_property_name = full_property_name
        self.__parent_property = parent_property

    def __getattr__(self, item: str) -> Any:
        if item.startswith("__") and item.endswith("__"):
            raise AttributeError

        if item == "_YamlMissing__parent_property":
            return self.__parent_property

        if item == "_YamlMissing__property_name":
            return self.__property_name

        if item == "_YamlMissing__full_property_name":
            return self.__property_name

        if item == "_YamlMissing__create_if_missing":
            return self.__create_if_missing

        # If we get calls for other attributes, we just return none
        return YamlMissing(
            parent_property=self,
            property_name=item,
            full_property_name=f"{self.__full_property_name}.{item}",
        )

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setattr__(self, key, value) -> None:
        if key == "_YamlMissing__property_name":
            super(YamlMissing, self).__setattr__(key, value)
            return

        if key == "_YamlMissing__parent_property":
            super(YamlMissing, self).__setattr__(key, value)
            return

        if key == "_YamlMissing__full_property_name":
            super(YamlMissing, self).__setattr__(key, value)
            return

        if self.__parent_property is None:
            raise Exception(f"No parent_property set on the missing property {self}")

        parent: YamlDict = self.__parent_property.__create_if_missing()

        if self.__property_name in parent:
            container = parent[self.__property_name]
        else:
            container = dict()
            parent[self.__property_name] = container

        container[key] = value

    def __create_if_missing(self) -> "YamlDict":
        if self.__parent_property is None:
            raise Exception(f"No parent_property set on the missing property {self}")

        parent: YamlDict = self.__parent_property.__create_if_missing()

        if self.__property_name in parent:
            return parent[self.__property_name]

        container: Dict[str, Any] = dict()
        parent[self.__property_name] = container

        return YamlDict(
            property_name=self.__property_name,
            content=container,
        )

    def __setitem__(self, key, value) -> None:
        self.__setattr__(key, value)

    def _raw(self) -> Any:
        return None

    def __len__(self):
        return 0

    def __iter__(self):
        return YamlMissing.EMPTY_LIST.__iter__()

    def __repr__(self):
        return f"YamlMissing({self.__full_property_name})"

    def __deepcopy__(self, memodict={}):
        return YamlMissing(
            parent_property=None,  # FIXME: this means assignment won't work anymore
            property_name=self.__property_name,
            full_property_name=self.__full_property_name,
        )


from yamldict.YamlDictClass import YamlDict
