import termcolor_util
from adhesive import config


def yellow(text: str, bold=False, underline=False) -> str:
    if not config.current.boolean.color:
        return text

    return termcolor_util.yellow(text, bold=bold, underline=underline)


def green(text: str, bold=False, underline=False) -> str:
    if not config.current.boolean.color:
        return text

    return termcolor_util.green(text, bold=bold, underline=underline)


def red(text: str, bold=False, underline=False) -> str:
    if not config.current.boolean.color:
        return text

    return termcolor_util.red(text, bold=bold, underline=underline)


def white(text: str, bold=False, underline=False) -> str:
    if not config.current.boolean.color:
        return text

    return termcolor_util.white(text, bold=bold, underline=underline)

