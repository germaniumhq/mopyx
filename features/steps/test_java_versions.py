from behave import use_step_matcher, step
from unittest import TestCase
import subprocess
import re

test_case = TestCase()
test_case.maxDiff = None
assertEqual = test_case.assertEqual
assertFalse = test_case.assertFalse

VERSION_MATCHER = re.compile('^Python ((\d+\.\d+)\.\d+)')

use_step_matcher("re")


@step("I run the docker container for '(.*)'")
def run_docker_container(context, container_name: str) -> None:
    context.container_name = container_name


@step("I get as output '(.*)'")
def check_expected_output(context, expected):
    assertEqual(expected, context.docker_output)


@step("I get as version '(.*)'")
def check_expected_version(context, version):
    for line in context.docker_output.split('\n'):  # type: str
        if re.match('\w+ version "%s_\d+"' % re.escape(version), line):
            return

    assertFalse(True, "Unable to find version %s in text: %s" % (version, context.docker_output))


@step("I get the version of the default java command")
def get_python_version(context) -> None:
    run_docker_command(context, "java -version")


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

    output = subprocess.check_output(program)  # type: bytes
    context.docker_output = output.decode('utf-8').strip()


@step("it is version '(.*)'")
def check_python_version(context, container_name: str) -> None:
    m = VERSION_MATCHER.match(context.docker_output)
    if not m:
        raise Exception("Unable to parse version from: %s" % context.docker_output)

    context.python_version = m.group(2)

    assertEqual(container_name, context.python_version)
