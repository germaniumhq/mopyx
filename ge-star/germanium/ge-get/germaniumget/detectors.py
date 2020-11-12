import os
import sys
import re

from germaniumget.styles import warning
from germaniumget.execute_program import execute_program


def is_edge_detected():
    return is_program_in_folder(r"C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe",
                                "MicrosoftEdge")


def is_chrome_detected():
    return is_program_in_classpath("google-chrome")


def is_firefox_detected():
    return is_program_in_classpath("firefox")


def is_java8_installed():
    return is_program_in_classpath("java") \
        and program_execution_matches(
            ["java", "-version"],
            r'java version "1.8.\d+_\d+')


def is_program_in_classpath(program_name):
    """
    Check if the program is in the classpath.
    """
    for path_entry in os.environ['PATH'].split(os.pathsep):
        if is_program_in_folder(path_entry, program_name):
            return True

    return None


def is_program_in_folder(folder, program_name):
    if sys.platform.startswith("win"):
        program_name += ".EXE"

    full_path = os.path.join(folder, program_name)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return True

    return False


def program_execution_matches(program, searched_pattern):
    """
    Checks if the executed program contains the serched pattern (expressed as a
    regex).
    """
    pattern = re.compile(searched_pattern, re.MULTILINE)
    stdout = execute_program(program)

    print(warning(stdout))

    return bool(pattern.search(stdout))

