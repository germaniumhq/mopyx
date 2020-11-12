from typing import Callable, Any, Optional

from adhesive.execution import token_utils
from adhesive.execution.ExecutionBaseTask import ExecutionBaseTask, RegexList, ExpressionList
from adhesive.execution.ExecutionToken import ExecutionToken
from adhesive.logredirect.LogRedirect import redirect_stdout
from adhesive.model.ActiveEvent import ActiveEvent


class ExecutionUserTask(ExecutionBaseTask):
    """
    A task implementation.
    """
    def __init__(self,
                 *args,
                 code: Callable,
                 expressions: ExpressionList,
                 regex_expressions: RegexList,
                 loop: Optional[str] = None,
                 when: Optional[str] = None,
                 lane: Optional[str] = None,
                 deduplicate: Optional[str] = None,
            ) -> None:
        if args:
            raise Exception("You need to pass in the arguments by name")

        super(ExecutionUserTask, self).__init__(
            code=code,
            expressions=expressions,
            regex_expressions=regex_expressions,
            deduplicate=deduplicate,
        )

        self.loop = loop
        self.when = when
        self.lane = lane

    def invoke_usertask(
            self,
            event: ActiveEvent,
            ui: Any) -> ExecutionToken:
        with redirect_stdout(event):
            params = token_utils.matches(
                    self.re_expressions,
                    event.context.task_name)

            self.code(event.context, ui, *params)  # type: ignore

            return event.context

    def __repr__(self) -> str:
        return f"@usertask(expressions={self.expressions}, code={self.code.__name__})"
