import os
import re
import subprocess
import sys
import textwrap

from termcolor_util import red, yellow, cyan

from git_monorepo.git_monorepo_config import (
    read_monorepo_config,
    MONOREPO_CONFIG_FILE,
    write_synchronized_commits,
    _resolve_in_repo,
    get_current_commit,
    GitMonorepoConfig,
)


def move(old_path: str, new_path: str) -> None:
    """
    git mv old/path new/path
    """
    monorepo = read_monorepo_config()

    old_path = _resolve_in_repo(monorepo, old_path)
    new_path = _resolve_in_repo(monorepo, new_path)

    if old_path not in monorepo.repos:
        print(
            red(old_path, bold=True),
            red("not defined in"),
            red(MONOREPO_CONFIG_FILE, bold=True),
        )
        sys.exit(1)

    print(
        cyan("moving"), cyan(old_path, bold=True), cyan("->"), cyan(new_path, bold=True)
    )

    current_commit = get_current_commit(project_folder=monorepo.project_folder)
    remote_commit = get_remote_commit(monorepo=monorepo, old_path=old_path)

    if monorepo.squash:
        message = textwrap.dedent(
            f"""\
            git-monorepo: move {old_path} -> {new_path}
            
            git-subtree-dir: {new_path}
            git-subtree-split: {remote_commit}
        """
        )
    else:
        # FIXME: I'm not sure about the mainline thing, it is supposed
        #        to be the commit in the current tree, presumably for the
        #        subtree to have an easier time to decide what commits
        #        get in.
        message = textwrap.dedent(
            f"""\
            git-monorepo: move {old_path} -> {new_path}

            git-subtree-dir: {new_path}
            git-subtree-mainline: {current_commit}
            git-subtree-split: {remote_commit}
        """
        )

    # we ensure the path exists
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    subprocess.check_call(
        ["git", "mv", old_path, new_path], cwd=monorepo.project_folder
    )

    subprocess.check_call(
        ["git", "commit", "-m", message],
        cwd=monorepo.project_folder,
    )

    monorepo.repos[new_path] = monorepo.repos[old_path]
    del monorepo.repos[old_path]

    # FIXME: probably wrong location, and wrong commit
    write_synchronized_commits(monorepo, repo=new_path)

    print(
        "⚠️ ⚠️ ⚠️ ",
        yellow("WARNING", bold=True),
        "⚠️ ⚠️ ⚠️ ",
        yellow("don't forget to patch"),
        yellow(MONOREPO_CONFIG_FILE, bold=True),
        yellow("with the new location, and remove the old entry"),
    )


def get_remote_commit(*, monorepo: GitMonorepoConfig, old_path: str) -> str:
    log = subprocess.check_output(
        ["git", "log", "."], cwd=monorepo.project_folder
    ).decode("utf-8")

    SUBTREE_DIR_RE = re.compile(
        r"^\s*" + re.escape(f"git-subtree-dir: {old_path}") + "$"
    )
    SUBTREE_COMMIT_RE = re.compile(r"^\s*git-subtree-split:\s*([0-9a-f]+)$")

    found_commit = False
    for line in log.splitlines():
        if not found_commit:
            subtree_match = SUBTREE_DIR_RE.match(line)
            if subtree_match:
                found_commit = True

            continue

        m = SUBTREE_COMMIT_RE.match(line)
        if m:
            return m.group(1)

    print(red(f"Unable to find any subtree commit for", red(old_path, bold=True)))
    sys.exit(1)
