from .util.find_germanium_object import find_germanium_object


def iframe(target, keep_new_context=False):
    """
    IFrame selector for various operations.
    :param target: The IFrame to set.
    :param keep_new_context: True if the new IFrame should be kept as context after the method is done.
    :param germanium:
    :return:
    """
    def wrapper(original):
        def original_aspect(*args, **kwargs):
            germanium = find_germanium_object(args)
            original_iframe = germanium.current_iframe

            germanium.select_iframe(target)

            try:
                return original(*args, **kwargs)
            finally:
                if not keep_new_context:
                    germanium.select_iframe(original_iframe)

        return original_aspect

    return wrapper
