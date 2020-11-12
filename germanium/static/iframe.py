from .global_germanium_instance import get_instance


def iframe(target="default", keep_new_context=False):
    """
    Switch the iframe in static contexts.
    :param target: The IFrame identifier that will be passed to the iframe strategy.
    :param keep_new_context: Don't restore to the old iframe when the function returns.
    """
    def wrapper(original):
        def original_aspect(*args, **kwargs):
            germanium = get_instance()
            original_iframe = germanium.current_iframe

            germanium.select_iframe(target)

            try:
                return original(*args, **kwargs)
            finally:
                if not keep_new_context:
                    germanium.select_iframe(original_iframe)

        return original_aspect

    return wrapper
