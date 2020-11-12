import os
import subprocess
import unittest

from behave import step, use_step_matcher

use_step_matcher("re")
test = unittest.TestCase()


@step("I run adhesive on a process with a UT with a single checkbox")
def run_the_process_with_a_single_checkbox(contxt):
    subprocess.check_call(["python", "-m", "adhesive.mainapp"],
                          cwd=f"{os.getcwd()}/features/processes/single_checkbox")


@step("I run adhesive without UI redirection on '(.*?)'")
def run_without_ui_redirection(contxt, folder):
    subprocess.check_call(["python", "-m", "adhesive.mainapp"],
                          cwd=f"{os.getcwd()}/features/{folder}")


@step("I run adhesive on '(.*?)'")
def run_an_adhesive_process(context, folder):
    pipes = subprocess.Popen(
        ["python", "-m", "adhesive.mainapp"],
        cwd=f"{os.getcwd()}/features/{folder}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = pipes.communicate()
    context.pipes = pipes

    context.process_return_code = pipes.returncode
    context.process_stdout = stdout.decode("utf-8")
    context.process_stderr = stderr.decode("utf-8")


@step("the adhesive process has failed")
def the_adhesive_process_has_failed(context):
    assert context.process_return_code != 0


@step("the adhesive process has passed")
def the_adhesive_process_has_passed(context):
    print("STDOUT", context.process_stdout)
    print("STDERR", context.process_stderr)
    assert context.process_return_code == 0


@step("there is in the (.*?) the text '(.*?)'")
def check_the_text_in_stdouterr(context, where, searched_text):
    print("STDOUT")
    print(context.process_stdout)
    print("STDERR")
    print(context.process_stderr)

    if where == "stdout":
        assert searched_text in context.process_stdout
    else:
        assert searched_text in context.process_stderr


@step("there isn't in the (.*?) the text '(.*?)'")
def check_the_text_in_stdouterr(context, where, searched_text):
    if where == "stdout":
        print("STDOUT")
        print(context.process_stdout)
        assert searched_text not in context.process_stdout
    else:
        print("STDERR")
        print(context.process_stderr)
        assert searched_text not in context.process_stderr


@step("the user task renders just fine")
def noop(context):
    pass


@step("the '(.*?)' is executed only once")
def task_executed_after_two_tasks(context,
                                  waiting_task: str) -> None:
    #raise Exception(f'Run  {waiting_task}')
    print(f'Run  {waiting_task}')
    print(f'STDOUT: {context.process_stdout}')
    test.assertEqual(
        1,
        context.process_stdout.count(f'Run  {waiting_task}')
    )

