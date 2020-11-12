from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Iterable, Union, Tuple


class UiBuilderApi(ABC):
    @abstractmethod
    def add_input_text(self,
                       name: str,
                       title: Optional[str] = None,
                       value: str = '') -> None:
        pass

    @abstractmethod
    def add_input_password(self,
                           name: str,
                           title: Optional[str] = None,
                           value: str = '') -> None:
        pass

    @abstractmethod
    def add_combobox(self,
                     name: str,
                     title: Optional[str] = None,
                     value: Optional[str]=None,
                     values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:
        pass

    @abstractmethod
    def add_checkbox_group(
            self,
            name: str,
            title: Optional[str]=None,
            value: Optional[Iterable[str]]=None,
            values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:
        pass

    @abstractmethod
    def add_radio_group(self,
                        name: str,
                        title: Optional[str]=None,
                        value: Optional[str]=None,
                        values: Optional[List[Any]]=None) -> None:
        pass

    @abstractmethod
    def add_default_button(self,
                           name: str,
                           title: Optional[str]=None,
                           value: Optional[Any]=None) -> None:
        pass
