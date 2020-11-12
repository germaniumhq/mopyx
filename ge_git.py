from typing import Optional
import re


TAG_VERSION = re.compile("^\\d+\\.\\d+(\\.\\d+)?$")


def is_master_branch(version: str) -> bool:
    return version == "master"


def get_tag_version(version: str) -> Optional[str]:
    """
    Returns the version if it matches, else it returns None.
    """
    m = TAG_VERSION.match(version)

    if not m:
        return None

    return m.group(0)


def is_changed_repo(context) -> bool:
    """
    Checks if the current repository has changed files
    """

    changed_files: str = context.workspace.run_output("""
        git diff-index HEAD --
    """)

    return not not changed_files.strip()
