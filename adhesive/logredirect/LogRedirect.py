import os
import sys
from contextlib import contextmanager
from threading import local
from typing import Union, Any, TextIO, cast

from adhesive.logredirect import is_enabled
from adhesive.model.ActiveEvent import ActiveEvent

# Save the original stdout/stderr. This is what we initialize our
# threadlocal, so python stays always happy on every thread.
python_stdout = sys.stdout
python_stderr = sys.stderr


# We inherit the threading.local in order to have initialization
# of the variables happening in the new constructor.
class StdThreadLocal(local):
    """
    A thread local object that implicitly initializes the newly
    created threads with data. In this case it's the orginal
    python stdout and stderr objects.
    """
    def __init__(self):
        super(StdThreadLocal, self).__init__()

        self.stdout = python_stdout
        self.stderr = python_stderr


# The data that's shared by the threads in order to have the
# output redirected per each individual task.
data = StdThreadLocal()


class ObjectForward:
    """
    Redirects everything to the object stored in the threadlocal.
    This is use to replace the sys.stdout/stderr, and to have
    an object that delegates to the threadlocal instance.
    """
    def __init__(self, key: str) -> None:
        self.__key = key

    def __getattribute__(self, key: str) -> Any:
        if key == "_ObjectForward__key":
            return super(ObjectForward, self).__getattribute__(key)

        return data.__getattribute__(self.__key).__getattribute__(key)

    def __setattr__(self, key: str, value: Any) -> None:
        if key == "_ObjectForward__key":
            return super(ObjectForward, self).__setattr__(key, value)

        data[self.__key].__setattr__(key, value)  # type: ignore


sys.stdout = cast(TextIO, ObjectForward("stdout"))
sys.stderr = cast(TextIO, ObjectForward("stderr"))


class StreamLogger:
    """
    Redirects a stream output to a file. Since we can't intercept
    subprocess redirections - because they use the native file handle
    to write the output, we redirect all the content to the file.
    """
    def __init__(self,
                 name: str,
                 folder: str) -> None:
        if not folder:
            raise Exception(f"No folder specified for output: {folder}")

        self.log = open(
            os.path.join(folder, name),
            "at")

        self._closed = False

    @staticmethod
    def from_event(event: Union[ActiveEvent, str],
                   name: str) -> 'StreamLogger':
        folder = ensure_folder(event)
        return StreamLogger(name, folder)

    @property
    def fileno(self):
        return self.log.fileno

    def flush(self):
        self.log.flush()

    def write(self, message):
        if self._closed:
            raise Exception("already closed")

        self.log.write(message)
        self.log.flush()

    def close(self) -> None:
        self.log.close()
        self._closed = True


@contextmanager
def redirect_stdout(event: Union[ActiveEvent, str]) -> Any:
    """
    Redirects the stdout/stderr to a file.
    """
    if not is_enabled():
        yield None
        return

    old_stdout = data.stdout
    old_stderr = data.stderr

    # if we don't define them here, and we get an exception in the
    # stream redirect initialization, we can't check if they were
    # not initialized, and don't attempt to close() the streams.
    new_stdout = None
    new_stderr = None

    try:
        new_stdout = StreamLogger.from_event(event, "stdout")
        new_stderr = StreamLogger.from_event(event, "stderr")

        data.stdout = new_stdout
        data.stderr = new_stderr

        yield None
    finally:
        data.stdout = old_stdout
        data.stderr = old_stderr

        if new_stdout:
            new_stdout.close()

        if new_stderr:
            new_stderr.close()


from adhesive.storage.task_storage import ensure_folder

