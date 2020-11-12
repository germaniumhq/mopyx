from typing import cast

from adhesive.graph.ScriptTask import ScriptTask
from adhesive.logredirect.LogRedirect import redirect_stdout
from adhesive.model.ActiveEvent import ActiveEvent
from adhesive.execution.ExecutionToken import ExecutionToken
from adhesive.execution import token_utils


def call_script_task(event: ActiveEvent) -> ExecutionToken:
    with redirect_stdout(event):
        eval_data = token_utils.get_eval_data(event.context)
        exec(
            cast(ScriptTask, event.task).script,
            {},                          # globals
            eval_data)
        return event.context
