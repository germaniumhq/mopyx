import abc
from typing import TypeVar, Generic

T = TypeVar("T")


class YamlNavigator(abc.ABC, Generic[T]):
    @abc.abstractproperty
    def _raw(self) -> T:
        """
        Gets access to the underlying collection.
        :return:
        """
        raise Exception("Not implemented")

    @abc.abstractmethod
    def __len__(self) -> int:
        raise Exception("Not implemented")

    @abc.abstractmethod
    def __iter__(self):
        raise Exception("Not implemented")
