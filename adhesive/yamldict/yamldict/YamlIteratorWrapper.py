from typing import Iterator, Any, ItemsView


class YamlIteratorWrapper:
    def __init__(self, *, property_name: str, iter: Iterator):
        self._property_name = property_name
        self._iter = iter

    def __iter__(self):
        return YamlIteratorWrapper(property_name=self._property_name, iter=self._iter)

    def __next__(self):
        result = self._iter.__next__()

        return convert_type(
            property_name=f"{self._property_name}._iterator", value=result
        )


class YamlDictIteratorWrapper:
    def __init__(self, *args, property_name: str, iter: Iterator):
        if args:
            raise Exception("You need to pass the arguments by name")

        self._property_name = property_name
        self._iter = iter

    def __iter__(self):
        return YamlDictIteratorWrapper(
            property_name=self._property_name, iter=self._iter
        )

    def __next__(self):
        result = self._iter.__next__()

        return (
            result[0],
            convert_type(
                property_name=f"{self._property_name}.{result[0]}",
                value=result[1],
            ),
        )


class YamlDictWrapper:
    def __init__(self, *args, property_name: str, items_view: ItemsView):
        if args:
            raise Exception("You need to pass the arguments by name")

        self._property_name = property_name
        self._items_view = items_view

    def __iter__(self):
        return YamlDictIteratorWrapper(
            property_name=self._property_name,
            iter=self._items_view.__iter__(),
        )


def convert_type(*, property_name: str, value: Any) -> Any:
    if isinstance(value, dict):
        return YamlDict(property_name=property_name, content=value)
    elif isinstance(value, list):
        return YamlList(property_name=property_name, content=value)

    return value


from yamldict.YamlDictClass import YamlDict
from yamldict.YamlListClass import YamlList
