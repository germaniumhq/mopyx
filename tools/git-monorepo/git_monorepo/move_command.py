import os
import subprocess
import sys

from termcolor_util import red, yellow, cyan

from git_monorepo.git_monorepo_config import (
    read_monorepo_config,
    MONOREPO_CONFIG_FILE,
    write_synchronized_commits,
    _resolve_in_repo,
)
from git_monorepo.git_util import env_extend


def move(old_path: str, new_path: str) -> None:
    """
    git mv old/path new/path
    git subtree split --rejoin --prefix=new/path HEAD
    git subtree pull --squash --prefix=new/path giturl branch
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

    giturl = monorepo.repos[old_path]

    print(
        cyan("moving"), cyan(old_path, bold=True), cyan("->"), cyan(new_path, bold=True)
    )

    # we ensure the path exists
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    subprocess.check_call(
        ["git", "mv", old_path, new_path], cwd=monorepo.project_folder
    )

    subprocess.check_call(
        ["git", "commit", "-m", f"git-monorepo: move {old_path} -> {new_path}"],
        cwd=monorepo.project_folder,
    )

    subprocess.check_call(
        ["git", "subtree", "split", "--rejoin", f"--prefix={new_path}", "HEAD"],
        cwd=monorepo.project_folder,
        env=env_extend(
            {
                "EDITOR": "git-monorepo-editor",
                "GIT_MONOREPO_EDITOR_MESSAGE": f"git-monorepo: Sync {new_path}",
            }
        ),
    )

    subprocess.check_call(
        [
            "git",
            "subtree",
            "pull",
            "--squash",
            f"--prefix={new_path}",
            giturl,
            monorepo.current_branch,
        ],
        cwd=monorepo.project_folder,
        env=env_extend(
            {
                "EDITOR": "git-monorepo-editor",
                "GIT_MONOREPO_EDITOR_MESSAGE": f"git-monorepo: Sync {new_path}",
            }
        ),
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
