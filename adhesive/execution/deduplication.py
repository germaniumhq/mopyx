import logging
from typing import cast

import addict

from adhesive.execution.token_utils import get_eval_data
from adhesive.graph.ProcessTask import ProcessTask
from adhesive.model.ActiveEvent import ActiveEvent

LOG = logging.getLogger(__name__)


def update_deduplication_id(
    event: ActiveEvent,
) -> None:
    if not isinstance(event.task, ProcessTask):
        return

    expression = cast(ProcessTask, event.task).deduplicate

    if expression is None:
        return

    eval_data = addict.Dict(get_eval_data(event.context))
    deduplication_id = eval(
        expression,
        {},
        eval_data)

    if not deduplication_id:
        LOG.warning(f"Deduplication returned a falsy object for {expression}. "
                    f"The return was {deduplication_id}.")

    event.deduplication_id = deduplication_id
