from contextlib import contextmanager
from typing import Callable, TypeVar, Optional, Union, List, Generator, Any, cast, IO, TextIO

from adhesive import config
from adhesive.consoleui.ConsoleUserTaskProvider import ConsoleUserTaskProvider
from adhesive.execution.ExecutionLane import ExecutionLane
from adhesive.execution.ExecutionMessageCallbackEvent import ExecutionMessageCallbackEvent
from adhesive.execution.ExecutionMessageEvent import ExecutionMessageEvent
from adhesive.execution.ExecutionTask import ExecutionTask
from adhesive.execution.ExecutionToken import ExecutionToken
from adhesive.execution.ExecutionUserTask import ExecutionUserTask
from adhesive.graph.ProcessTask import ProcessTask
from adhesive.logging import configure_logging
from adhesive.model.AdhesiveProcess import AdhesiveProcess
from adhesive.model.ProcessExecutor import ProcessExecutor
from adhesive.model.UiBuilderApi import UiBuilderApi
from adhesive.process_read.bpmn import read_bpmn_file
from adhesive.process_read.programmatic import generate_from_calls
from adhesive.process_read.tasks import generate_from_tasks
from adhesive.workspace.Workspace import Workspace

T = TypeVar('T')
V = TypeVar('V')

process = AdhesiveProcess('_root')


UI = UiBuilderApi

class Token(ExecutionToken[T]):
    workspace: Workspace
    task: ProcessTask


_DecoratedFunction = Union[  # FIXME: this is terrible
    Callable[[Token[T]], V],
    Callable[[Token[T], str], V],
    Callable[[Token[T], str, str], V],
    Callable[[Token[T], str, str, str], V],
    Callable[[Token[T], str, str, str, str], V],
]

_DecoratedUiFunction = Union[  # FIXME: this is terrible
    Callable[[Token[T], UI], V],
    Callable[[Token[T], UI, str], V],
    Callable[[Token[T], UI, str, str], V],
    Callable[[Token[T], UI, str, str, str], V],
    Callable[[Token[T], UI, str, str, str, str], V],
]

_DecoratedCallbackFunction = Union[  # FIXME: this is terrible
    Callable[[Token[T], Callable[[Any], None]], V],
    Callable[[Token[T], Callable[[Any], None], str], V],
    Callable[[Token[T], Callable[[Any], None], str, str], V],
    Callable[[Token[T], Callable[[Any], None], str, str, str], V],
    Callable[[Token[T], Callable[[Any], None], str, str, str, str], V],
]

WorkspaceGenerator = Generator[Workspace, Workspace, None]
MessageGenerator = Generator[Any, Any, None]

LaneFunction = _DecoratedFunction[T, WorkspaceGenerator]
MessageFunction = _DecoratedFunction[T, MessageGenerator]

#FIXME: move decorators into their own place


def task(*task_names: str,
         re: Optional[Union[str, List[str]]] = None,
         loop: Optional[str] = None,
         when: Optional[str] = None,
         lane: Optional[str] = None,
         deduplicate: Optional[str] = None,
         ) -> Callable[[_DecoratedFunction[T, None]], _DecoratedFunction[T, None]]:
    def wrapper_builder(f: _DecoratedFunction[T, None]) -> _DecoratedFunction[T, None]:
        task = ExecutionTask(
            code=f,
            expressions=task_names,
            regex_expressions=re,
            loop=loop,
            when=when,
            lane=lane,
            deduplicate=deduplicate,
        )

        process.task_definitions.append(task)
        process.chained_task_definitions.append(task)

        return f

    return wrapper_builder


gateway = task


def usertask(*task_names: str,
             re: Optional[Union[str, List[str]]] = None,
             loop: Optional[str] = None,
             when: Optional[str] = None,
             lane: Optional[str] = None,
             deduplicate: Optional[str] = None,
        ) -> Callable[[_DecoratedUiFunction[T, None]], _DecoratedUiFunction[T, None]]:
    def wrapper_builder(f: _DecoratedUiFunction[T, None]) -> _DecoratedUiFunction[T, None]:
        usertask = ExecutionUserTask(
            code=f,
            expressions=task_names,
            regex_expressions=re,
            loop=loop,
            when=when,
            lane=lane,
            deduplicate=deduplicate,
        )
        process.user_task_definitions.append(usertask)
        process.chained_task_definitions.append(usertask)
        return f

    return wrapper_builder


def lane(*lane_names:str,
         re: Optional[Union[str, List[str]]] = None,
         ) -> Callable[[LaneFunction], WorkspaceGenerator]:
    """
    Allow defining a lane where a custom workspace will be created. This
    function needs to yield a workspace that will be used. It's a
    contextmanager. When all the execution tokens exit the lane, the code after
    the yield will be executed.
    """
    def wrapper_builder(f: LaneFunction) -> WorkspaceGenerator:
        newf: WorkspaceGenerator = cast(WorkspaceGenerator, contextmanager(f))
        process.lane_definitions.append(ExecutionLane(
            code=newf,  # type: ignore
            expressions=lane_names,
            regex_expressions=re))
        return newf

    return wrapper_builder


def message(*message_names: str,
             re: Optional[Union[str, List[str]]] = None) -> Callable[[MessageFunction], MessageFunction]:
    def wrapper_builder(f: MessageFunction) -> MessageFunction:
        message_definition = ExecutionMessageEvent(
            code=f,
            expressions=message_names,
            regex_expressions=re)

        process.message_definitions.append(message_definition)

        return f

    return wrapper_builder


def message_callback(*message_names: str,
                     re: Optional[Union[str, List[str]]] = None) \
        -> Callable[[_DecoratedCallbackFunction], _DecoratedCallbackFunction]:
    """
    Obtain a message callback, that can push the
    :param message_names:
    :param re:
    :return:
    """
    def wrapper_builder(f: _DecoratedCallbackFunction) -> _DecoratedCallbackFunction:
        message_definition = ExecutionMessageCallbackEvent(
            code=f,
            expressions=message_names,
            regex_expressions=re)

        process.message_callback_definitions.append(message_definition)

        return f

    return wrapper_builder


# FIXME: move builders into their own place

def build(ut_provider: Optional['UserTaskProvider'] = None,
          wait_tasks: bool = True,
          initial_data = None):
    process.process = generate_from_tasks(process)

    return _build(ut_provider=ut_provider,
                  wait_tasks=wait_tasks,
                  initial_data=initial_data)


def process_start():
    builder = generate_from_calls(_build)
    process.process = builder.process

    return builder


def bpmn_build(file_name: Union[str, IO[bytes], TextIO],
               ut_provider: Optional['UserTaskProvider'] = None,
               wait_tasks: bool = True,
               initial_data = None):
    """ Start a build that was described in BPMN """
    process.process = read_bpmn_file(file_name)

    return _build(ut_provider=ut_provider,
                  wait_tasks=wait_tasks,
                  initial_data=initial_data)


def _build(ut_provider: Optional['UserTaskProvider'] = None,
           wait_tasks: bool = True,
           initial_data=None):

    configure_logging(config.current)

    if ut_provider is None:
        ut_provider = ConsoleUserTaskProvider()

    return ProcessExecutor(
        process,
        ut_provider=ut_provider,
        wait_tasks=wait_tasks).execute(initial_data=initial_data)


from adhesive.model.UserTaskProvider import UserTaskProvider
