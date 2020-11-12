import logging
import uuid
from concurrent.futures import Future
from threading import Thread

from adhesive.consoleui.color_print import green, red, yellow
from adhesive.execution import token_utils
from adhesive.execution.ExecutionMessageEvent import ExecutionMessageEvent
from adhesive.graph.MessageEvent import MessageEvent
from adhesive.model.ActiveEvent import ActiveEvent

LOG = logging.getLogger(__name__)


class MessageEventExecutor:
    def __init__(self,
                 root_event: ActiveEvent,
                 message_event: MessageEvent,
                 execution_message_event: ExecutionMessageEvent,
                 enqueue_event) -> None:
        self.id = str(uuid.uuid4())

        self.root_event = root_event.clone(message_event, None)  # Used only to print the task name
        self.execution_message_event = execution_message_event
        self.enqueue_event = enqueue_event

        # Future used to signal the termination of the message ingestion, so the
        # process can finish.
        self.future: Future = Future()

        thread = Thread(target=self.run_thread_loop)
        thread.setDaemon(True)

        thread.start()

    def run_thread_loop(self):
        # HACK: Here we need to use the token_utils.parse_name, since the actual
        # event handler uses the context of the root_event, and that one is bounded
        # to the [root process] task.
        event_name_parsed = token_utils.parse_name(
            self.root_event.context,
            self.root_event.task.name)

        LOG.info(yellow("Run  ") + yellow(event_name_parsed, bold=True))

        # FIXME: implement a decent test
        try:
            params = token_utils.matches(self.execution_message_event.re_expressions,
                                         event_name_parsed)

            for event_data in self.execution_message_event.code(self.root_event.context, *params):
                self.enqueue_event(
                    event=self.root_event.task,
                    event_data=event_data
                )
        except Exception as e:
            LOG.error(red("Failed ") + red(event_name_parsed, bold=True))
            LOG.error(e)
            self.future.set_exception(e)
        else:
            LOG.info(green("Done ") + green(event_name_parsed, bold=True))
            self.future.set_result("__done")
