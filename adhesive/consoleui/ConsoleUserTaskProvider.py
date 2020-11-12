import uuid
from typing import Optional, List, Dict, Any, Tuple, Union, Iterable, Set, Callable

import npyscreen as npyscreen

from adhesive.execution.ExecutionData import ExecutionData
from adhesive.model.ActiveEvent import ActiveEvent
from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.model.UiBuilderApi import UiBuilderApi
from adhesive.model.UserTaskProvider import UserTaskProvider


class UiBuilderButton:
    def __init__(self,
                 name: str,
                 label: Optional[str] = None,
                 value: Optional[Any] = None) -> None:
        self.name = name
        self.label = label
        self.value = value


DEFAULT_BUTTONS: List[UiBuilderButton] = [
    UiBuilderButton("ok_button", label="OK"),
]


class ConsoleUserTaskFormButton(npyscreen.wgbutton.MiniButtonPress):
    pass


class ConsoleUserTaskForm(npyscreen.ActionFormMinimal):
    def __init__(self,
                 ui_builder: 'UIBuilder',
                 name: str) -> None:
        self.ui_builder = ui_builder
        super(ConsoleUserTaskForm, self).__init__(name=name)

    def create_control_buttons(self):
        current_offset = -6

        button_names: Set[str] = set()
        same_name_buttons = False

        for button in self.ui_builder.buttons:
            if button.name in button_names:
                same_name_buttons = True
                break

            button_names.add(button.name)

        for button in reversed(self.ui_builder.buttons):
            label = self._create_button(button, same_name_buttons, current_offset)
            current_offset -= len(label) + 2

    def _create_button(self,
                       button: UiBuilderButton,
                       same_name_buttons: bool,
                       current_offset: int) -> str:
        def button_function():
            self.editing = False
            self.ui_builder.selected_button = button

        if button.label:
            label = button.label
        elif button.value is None:
            label = button.name
        elif same_name_buttons:
            label = button.value
        else:
            label = button.name

        self._add_button(
            str(uuid.uuid4()),
            ConsoleUserTaskFormButton,
            label,
            -1,
            current_offset - len(label),
            button_function)

        return label


class UIBuilder(UiBuilderApi):
    def __init__(self,
                 event: ActiveEvent):
        self.context = event.context
        self.ui_controls: Dict[str, Any] = dict()

        self.labels: Dict[str, List[str]] = dict()
        self.values: Dict[str, List[str]] = dict()
        self.buttons = DEFAULT_BUTTONS
        self.selected_button = None

        self.ncurses_calls: List[Callable] = []

    @property
    def data(self) -> ExecutionData:
        result_dict = dict()

        for name, ui_control in self.ui_controls.items():
            if isinstance(self.ui_controls[name], npyscreen.TitleMultiSelect):
                result = {self.values[name][it] for it in ui_control.value}
                result_dict[name] = result
                continue

            if isinstance(self.ui_controls[name], npyscreen.TitleCombo):
                result = self.values[name][ui_control.value] if ui_control.value >= 0 else None
                result_dict[name] = result
                continue

            if isinstance(self.ui_controls[name], npyscreen.TitleSelectOne):
                result = self.values[name][ui_control.value[0]] if len(ui_control.value) > 0 else None
                result_dict[name] = result
                continue

            result_dict[name] = ui_control.value

        if self.buttons is not DEFAULT_BUTTONS:
            assert self.selected_button
            result_dict[self.selected_button.name] = self.selected_button.value

        return ExecutionData(result_dict)

    def add_input_text(self,
                       name: str,
                       title: Optional[str] = None,
                       value: str = '') -> None:
        if not name:
            raise Exception("You need to pass a name for the input.")

        if not title:
            title = name

        def ncurses_input_text_call():
            self.ui_controls[name] = self.form.add_widget(
                npyscreen.TitleText,
                name=title,
                value=value)

        self.ncurses_calls.append(ncurses_input_text_call)

    def add_input_password(self,
                       name: str,
                       title: Optional[str] = None,
                       value: str = '') -> None:
        if not name:
            raise Exception("You need to pass a name for the input.")

        if not title:
            title = name

        def ncurses_input_password_call():
            self.ui_controls[name] = self.form.add_widget(
                npyscreen.TitlePassword,
                name=title,
                value=value)

        self.ncurses_calls.append(ncurses_input_password_call)

    def add_combobox(
            self,
            name: str,
            title: Optional[str] = None,
            value: Optional[str]=None,
            values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:
        if not name:
            raise Exception("You need to pass a name for the input.")

        if not title:
            title = name

        self.values[name] = UIBuilder._get_values(values)
        self.labels[name] = UIBuilder._get_labels(values)

        _value = self.values[name].index(UIBuilder._get_value(value)) if value else -1

        def ncurses_add_combobox_call():
            self.ui_controls[name] = self.form.add_widget(
                npyscreen.TitleCombo,
                name=title,
                value=_value,
                values=self.labels[name])

        self.ncurses_calls.append(ncurses_add_combobox_call)

    def add_checkbox_group(
            self,
            name: str,
            title: Optional[str]=None,
            value: Optional[Iterable[str]]=None,
            values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:
        if not name:
            raise Exception("You need to pass a name for the input.")

        if not values:
            raise Exception("You need to pass in some values to display in the group.")

        if not title:
            title = name

        if value is None:
            value = []

        title_overflows = 0 if len(title) < 14 else 1

        self.values[name] = UIBuilder._get_values(values)
        self.labels[name] = UIBuilder._get_labels(values)

        def ncurses_add_checbox_group_call():
            self.ui_controls[name] = self.form.add_widget(
                npyscreen.TitleMultiSelect,
                name=title,
                value=[self.values[name].index(UIBuilder._get_value(v)) for v in value],
                max_height=max(len(values) + 1, 2) + title_overflows,
                scroll_exit=True,
                values=self.labels[name])

        self.ncurses_calls.append(ncurses_add_checbox_group_call)

    def add_radio_group(self,
                        name: str,
                        title: Optional[str]=None,
                        value: Optional[str]=None,
                        values: Optional[Iterable[Union[Tuple[str, str], str]]]=None) -> None:
        if not name:
            raise Exception("You need to pass a name for the input.")

        if not title:
            title = name

        title_overflows = 0 if len(title) < 14 else 1

        self.values[name] = UIBuilder._get_values(values)
        self.labels[name] = UIBuilder._get_labels(values)

        _value = self.values[name].index(UIBuilder._get_value(value)) if value is not None else -1

        def ncurses_add_radio_group_call():
            self.ui_controls[name] = self.form.add_widget(
                npyscreen.TitleSelectOne,
                name=title,
                max_height=max(len(values), 2) + title_overflows,
                scroll_exit=True,
                value=_value,
                values=self.labels[name])

        self.ncurses_calls.append(ncurses_add_radio_group_call)

    def add_default_button(self,
                           name: str,
                           title: Optional[str] = None,
                           value: Optional[Any] = True) -> None:
        if self.buttons is DEFAULT_BUTTONS:
            self.buttons = []

        self.buttons.append(UiBuilderButton(
            name,
            label=title,
            value=value))

    @staticmethod
    def _get_values(values) -> List[str]:
        result = []

        for value in values:
            if isinstance(value, str):
                result.append(value)
                continue

            result.append(value[0])

        return result

    @staticmethod
    def _get_value(value) -> str:
        if isinstance(value, str):
            return value

        return value[0]

    @staticmethod
    def _get_labels(values) -> List[str]:
        result = []

        for value in values:
            if isinstance(value, str):
                result.append(value)
                continue

            result.append(value[1])

        return result


class ConsoleUserTaskProvider(UserTaskProvider):
    def __init__(self):
        super(ConsoleUserTaskProvider, self).__init__()

    def register_event(self,
                       executor: ProcessExecutor,
                       event: ActiveEvent) -> None:

        ui = UIBuilder(event)

        adhesive_task = executor.user_tasks_impl[event.task.id]
        context = adhesive_task.invoke_usertask(event, ui)

        # redirecting logs, and initializing ncurses is prolly a bad idea
        # the code that generates the UI shouldn't be run in ncurses
        def run_on_curses(x):
            try:
                # build the UI components on ncurses:
                ui.form = ConsoleUserTaskForm(ui_builder=ui,
                                              name=event.task.name)

                for ncurses_call in ui.ncurses_calls:
                    ncurses_call()

                # call the actual UI
                ui.form.edit()

                # put the values in the data.
                context.data = ExecutionData.merge(context.data, ui.data)

                event.future.set_result(context)
            except Exception as e:
                event.future.set_exception(e)

        npyscreen.wrapper_basic(run_on_curses)
