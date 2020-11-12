
import time
from germanium.impl import _ensure_list


MAX_CLOSURE_RESOLVES=5


def _current_time_in_millis():
    return int(round(time.time() * 1000))


def _resolve_closure(closure):
    result = original_closure = closure

    for i in range(MAX_CLOSURE_RESOLVES):
        if not hasattr(result, '__call__'):
            return result

        result = closure()
        closure = result

    raise Exception("Unable to resolve function: %s in %s tries. Too much recursion." %
                    (original_closure, MAX_CLOSURE_RESOLVES))


def wait(closures, *extra_closures, while_not=None, timeout=10):
    """
    Executes a function given as argument every 400 milliseconds until it returns true.

    If it goes more than the timeout in seconds, then this function throws an exception.

    If the waiting closures throw exception, then it is assumed as a temporary false
    result, but the wait will continue. This is intentional so you can wait for an element
    even if the page is still loading.

    :param closures:
    :param while_not:
    :param timeout:
    :param extra_closures:
    """
    while_not = _ensure_list(while_not)
    closures = list(_ensure_list(closures))
    closures.extend(extra_closures)

    def closure_try_catch():
        for closure in closures:
            try:
                result = _resolve_closure(closure)
                if result:
                    return result
            except Exception as e:
                print("WARNING: waiting as false since: %s" % e)

    starting_time = _current_time_in_millis()
    current_time = starting_time
    delta = float(timeout) * 1000

    if delta <= 0:
        raise Exception("You need to specify a timeout that is greater than 0. The timeout is expressed in seconds.")

    closure_result = False

    while current_time - starting_time < delta:
        starting_closure_eval_time = current_time

        for while_not_closure in while_not:
            try:
                if _resolve_closure(while_not_closure()):
                    raise Exception("Waiting failed, since while_not condition matched")
            except Exception as e:
                raise Exception("Waiting failed, since while_not condition raised exception", e)

        closure_result = closure_try_catch()

        if closure_result:
            break

        current_time = _current_time_in_millis()
        ending_closure_eval_time = current_time

        # Execution times don't count, and must be substracted from the
        # potential delay.
        actual_execution_time = ending_closure_eval_time - starting_closure_eval_time

        # we do the sleep only if the execution time is quicker than 400ms,
        # otherwise we already waited for the response from the server.

        if actual_execution_time < 400:
            time.sleep(float(400 - actual_execution_time) / 1000.0)

    if not closure_result:
        raise Exception("Waiting has failed")


def waited(closures, *extra_closures, while_not=None, timeout=10):
    """
    Executes a function given as argument every 400 milliseconds until it returns something,
    and returns that something.

    If it goes more than the timeout in seconds, then this function returns `None`.

    If the waiting closures throw exception, then it is assumed as a temporary false
    result, but the wait will continue. This is intentional so you can wait for an element
    even if the page is still loading.

    :param closures:
    :param while_not:
    :param timeout:
    :param extra_closures:
    """
    while_not = _ensure_list(while_not)
    closures = list(_ensure_list(closures))
    closures.extend(extra_closures)

    def closure_try_catch():
        for closure in closures:
            try:
                result = _resolve_closure(closure)
                return result
            except Exception as e:
                print("WARNING: waiting as false since: %s" % e)

    starting_time = _current_time_in_millis()
    current_time = starting_time
    delta = float(timeout) * 1000

    if delta <= 0:
        raise Exception("You need to specify a timeout that is greater than 0. The timeout is expressed in seconds.")

    closure_result = False

    while current_time - starting_time < delta:
        starting_closure_eval_time = current_time

        for while_not_closure in while_not:
            try:
                if while_not_closure():
                    return None
            except Exception as e:
                print("Waiting failed, since while_not condition raised exception: %s" % e)
                return None

        closure_result = closure_try_catch()

        if closure_result:
            break

        current_time = _current_time_in_millis()
        ending_closure_eval_time = current_time

        # Execution times don't count, and must be subtracted from the
        # potential delay.
        actual_execution_time = ending_closure_eval_time - starting_closure_eval_time

        # we do the sleep only if the execution time is quicker than 400ms,
        # otherwise we already waited for the response from the server.

        if actual_execution_time < 400:
            time.sleep(float(400 - actual_execution_time) / 1000.0)

    if not closure_result:
        return None

    return closure_result
