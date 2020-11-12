from __future__ import print_function

from termcolor import colored
import textwrap
import re


def title(text):
    """ Gets the text colored a something white and bold. """
    return colored(text, "white", attrs=["bold"])


def text(text):
    return colored(text, "white")


def logo(text):
    return colored(text, "grey", attrs=["bold"])


def block(text):
    return colored(textwrap.dedent(text).strip(),
                   "grey",
                   attrs=["bold"])


def question(text):
    return colored(text, "cyan", attrs=["bold"])


def warning(text):
    return colored(text, "yellow")


def error(text):
    return colored(text, "red")


def option(text, default=False):
    m = re.match(r'^(.*?\[)(.*?)(\].*?)$', text)
    return colored(m.group(1), "white", attrs=["bold"] if default else None) + \
        colored(m.group(2), "white", attrs=["bold"] if default else None) + \
        colored(m.group(3), "white", attrs=["bold"] if default else None)


def options(*opts, **kw):
    default_value = opts[0]

    if "default" in kw:
        default_value = kw["default"]

    message = ""
    for opt in opts:
        message += option(opt, opt == default_value) + " "

    message += ": "

    return message


def read_option(*opts, **kw):
    default_value = opts[0]

    if "default" in kw:
        default_value = kw["default"]

    while True:
        print(options(*opts, **kw), end="")
        result = input()

        for opt in opts:
            m = re.match(r'^(.*?)\[(.*?)\](.*?)$', opt)
            text = m.group(1) + m.group(2) + m.group(3)
            lower_text = text.lower()

            if lower_text == result.lower() or\
                    m.group(2).lower() == result.lower():  # the shortcut

                print(title(text))
                return lower_text

            if result == '' and default_value == opt:
                print(title(text))
                return lower_text

        print(error("Invalid input value: %s." % result))


def read_string(prompt, default=None):
    """ Read a full line string from the user. """
    if default:
        print(text("%s:" % prompt), end="")
    else:
        print(text("%s (%s):" % (prompt, default)), end="")

    result = input()

    if not result:
        print(title(default))
        return default

    print(title(result))
    return result
