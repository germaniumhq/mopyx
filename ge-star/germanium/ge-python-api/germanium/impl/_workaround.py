#
# Allow to create workarounds for broken implementation, and a way
# of managing them in case a specific browser has issues.
#
# The browser_check() will receive a germanium instance resolved
# from the current context.
#


def workaround(browser_check, replacement_code):
    """
    Checks the browser if the workaround applies, and if it
    does will execute the replacement code instead of the original
    function.

    The replacement code will receive the germanium instance
    on the first parameter, and the original_function as
    the second parameter, so it can default on calling it to
    easily test if the function was fixed upstream.

    :param browser_check:
    :param replacement_code:
    :return:
    """
    def wrapper(original):
        def original_aspect(*args, **kwargs):
            # Dhis will check if there is actually a germanium instance
            # passed to be workarounded. Some workarounds are based on
            # environment variable checks, and don't need a germanium instance.
            germanium = None

            if args:
                germanium = args[0]

            if browser_check(germanium):
                return replacement_code(germanium,
                                        original,
                                        *args,
                                        **kwargs)

            return original(*args, **kwargs)

        return original_aspect
    return wrapper
