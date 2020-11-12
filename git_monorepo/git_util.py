import os
import subprocess
from typing import Dict

from git_monorepo import git_monorepo_config


def env_extend(extra_env: Dict[str, str]) -> Dict[str, str]:
    result = dict(os.environ)
    result.update(extra_env)

    return result


def is_repo_unchanged(
    monorepo: "git_monorepo_config.GitMonorepoConfig", folder_name: str
) -> bool:
    """
    We check if the sub-repo is changed. This is done via a log that could happen
    against multiple branches if this is a merge.
    :param monorepo:
    :param folder_name:
    :return:
    """
    # if no commits are synchronized, we need to mark this repo as changed
    # first, so the changes are being pushed
    if (
        not monorepo.synchronized_commits
        or folder_name not in monorepo.synchronized_commits
    ):
        return False

    for last_commit in monorepo.synchronized_commits[folder_name]:
        folder_log = (
            subprocess.check_output(
                ["git", "log", f"{last_commit}..HEAD", "--", folder_name],
                cwd=monorepo.project_folder,
            )
            .decode("utf-8")
            .strip()
        )

        if folder_log:
            return False

    return True


def get_current_git_branch(project_folder: str) -> str:
    """
    Gets the branch name for a folder
    :param project_folder:
    :return:
    """
    return (
        subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=project_folder
        )
        .decode(encoding="utf-8")
        .strip()
    )
