from typing import Optional, List, Iterable, Union, Tuple, Any

from adhesive.model.ActiveEvent import ActiveEvent
from adhesive.model.UiBuilderApi import UiBuilderApi
from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.model.UserTaskProvider import UserTaskProvider
from adhesive.execution.ExecutionToken import ExecutionToken


class UIBuilder(UiBuilderApi):
    def __init__(self,
                 context: ExecutionToken):
        self.context = context

    def add_input_text(self,
                       name: str,
                       title: Optional[str] = None,
                       value: str = '') -> None:
        self.context.data[name] = name

    def add_input_password(self,
                           name: str,
                           title: Optional[str] = None,
                           value: str = '') -> None:
        self.context.data[name] = name

    def add_combobox(self,
                     name: str,
                     title: Optional[str] = None,
                     value: Optional[str]=None,
                     values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:
        self.context.data[name] = values[0]  # type: ignore

    def add_checkbox_group(
            self,
            name: str,
            title: Optional[str]=None,
            value: Optional[Iterable[str]]=None,
            values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:
        self.context.data[name] = value

    def add_radio_group(self,
                        name: str,
                        title: Optional[str]=None,
                        value: Optional[str]=None,
                        values: Optional[List[Any]]=None) -> None:
        pass

    def add_default_button(self,
                           name: str,
                           title: Optional[str]=None,
                           value: Optional[Any]=None) -> None:
        self.context.data[name] = name


class TestUserTaskProvider(UserTaskProvider):
    def register_event(self,
                       executor: ProcessExecutor,
                       event: ActiveEvent) -> None:
        assert event.future

        try:
            ui = UIBuilder(event.context)

            adhesive_task = executor.user_tasks_impl[event.task.id]
            context = adhesive_task.invoke_usertask(event, ui)

            event.future.set_result(context)
        except Exception as e:
            event.future.set_exception(e)

