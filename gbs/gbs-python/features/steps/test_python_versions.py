from behave import use_step_matcher, step
from unittest import TestCase
import subprocess
import re

assertEqual = TestCase().assertEqual

VERSION_MATCHER = re.compile(r'^Python ((\d+\.\d+)\.\d+)\s?.*$')
ANSI_CONTROL_CHARS_RE = re.compile(r'((\x9B|\x1B\[)[0-?]*[ -/]*[@-~])|(\x1B.)')

use_step_matcher("re")


def strip_ansi_control_chars(line: str) -> str:
    """
    Remove control characters such as colors, to make the parsing
    of the text easier.
    """
    return ANSI_CONTROL_CHARS_RE.sub('', line)


@step("I run the docker container for '(.*)'")
def run_docker_container(context, container_name: str) -> None:
    context.container_name = container_name


@step("I get as output '(.*)'")
def check_expected_output(context, expected):
    assertEqual(expected, context.docker_output)


@step("I get the version of the default python command")
def get_python_version(context) -> None:
    run_docker_command(context, "python --version")


@step("I get the version of the miniconda python command")
def get_miniconda_python_version(context) -> None:
    run_docker_command(context, "wine /germanium/wine/drive_c/Miniconda3/python.exe --version")


@step("I run in the container ['\"](.*)['\"]")
def run_docker_command(context, command: str):
    program = ['docker', 'run', '-t', '--rm', context.container_name]

    command_tokens = command.split("'")

    odd = True
    for command_token in command_tokens:
        if odd:
            # we break down parts of the command that is not between quotes,
            # and we strip trailing spaces.
            broken_down_token = filter(lambda it: it, command_token.split(" "))
            program.extend(broken_down_token)
        else:
            program.append(command_token)

        odd = not odd

    output: bytes = subprocess.check_output(program)
    str_output: str = output.decode('utf-8')
    str_output = strip_ansi_control_chars(str_output)

    context.docker_output = str_output.strip()


@step("it is version '(.*)'")
def check_python_version(context, container_name: str) -> None:
    m = VERSION_MATCHER.match(context.docker_output)

    if not m:
        raise Exception("Unable to parse version from: `%s`" % context.docker_output)

    context.python_version = m.group(2)

    assertEqual(container_name, context.python_version)
