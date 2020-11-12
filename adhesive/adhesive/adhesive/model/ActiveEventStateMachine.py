import logging
from enum import Enum

LOG = logging.getLogger(__name__)


class ActiveEventState(Enum):
    NEW = 'NEW'
    PROCESSING = 'PROCESSING'
    WAITING = 'WAITING'
    ERROR = 'ERROR'
    RUNNING = 'RUNNING'
    ROUTING = 'ROUTING'
    DONE_CHECK = 'DONE_CHECK'
    DONE_END_TASK = 'DONE_END_TASK'
    DONE = 'DONE'
