import os
import subprocess
import sys
from typing import Dict, Any, List, Optional

import yaml
from termcolor_util import red, yellow

from git_monorepo.git_util import get_current_git_branch, is_repo_unchanged

MONOREPO_CONFIG_FILE = "monorepo.yml"
MONOREPO_SYNC_FILE = ".monorepo.sync"


class GitMonorepoConfig:
    def __init__(
        self,
        *,
        repos: Dict[str, str],
        current_branch: str,
        synchronized_commits: Dict[str, List[str]],
        project_folder: str,
        squash: bool,
    ) -> None:
        # maps local folder to remote git repo location
        self.repos = repos
        self.current_branch = current_branch
        self.synchronized_commits = synchronized_commits
        self.project_folder = project_folder
        self.squash = squash


def read_monorepo_config() -> GitMonorepoConfig:
    monorepo_config_folder = os.path.abspath(os.curdir)
    while monorepo_config_folder and not os.path.isfile(
        os.path.join(monorepo_config_folder, MONOREPO_CONFIG_FILE)
    ):
        parent_folder = os.path.dirname(monorepo_config_folder)

        if parent_folder == monorepo_config_folder:
            print(
                red("Unable to find"),
                red(MONOREPO_CONFIG_FILE, bold=True),
                red("in any of the parents from"),
                red(os.path.abspath(os.curdir), bold=True),
            )
            sys.exit(1)

        monorepo_config_folder = parent_folder

    project_folder = monorepo_config_folder

    config_file_name = os.path.join(project_folder, MONOREPO_CONFIG_FILE)
    with open(config_file_name, "rt") as f:
        config_data = yaml.safe_load(f)

    if "branch" in config_data:
        current_branch = config_data["branch"]
    else:
        current_branch = get_current_git_branch(project_folder)

    squash = config_data.get("squash", True)

    synchronized_commits = _read_synchronized_commits(project_folder)

    repos: Dict[str, str] = dict()
    _merge_repos(path="", repos=repos, data=config_data["mappings"])

    return GitMonorepoConfig(
        repos=repos,
        current_branch=current_branch,
        project_folder=project_folder,
        synchronized_commits=synchronized_commits,
        squash=squash,
    )


def write_synchronized_commits(
    monorepo: GitMonorepoConfig,
    repo: str,
    commit: Optional[str] = None,
) -> None:
    sync_file_name = os.path.join(monorepo.project_folder, MONOREPO_SYNC_FILE)

    commit = (
        commit if commit else get_current_commit(project_folder=monorepo.project_folder)
    )

    # if no changes happened in the current repo, we don't update hashes for no reason
    if is_repo_unchanged(monorepo, repo):
        return

    monorepo.synchronized_commits[repo] = [commit]

    print(
        yellow("Updating"),
        yellow(sync_file_name, bold=True),
        yellow("for"),
        yellow(repo, bold=True),
    )

    with open(sync_file_name, "wt", encoding="utf-8") as f:
        yaml.safe_dump(monorepo.synchronized_commits, f)

    subprocess.check_call(
        ["git", "add", sync_file_name],
        cwd=monorepo.project_folder,
    )

    subprocess.check_call(
        [
            "git",
            "commit",
            "-m",
            f"git-monorepo: Sync commit hashes in {MONOREPO_SYNC_FILE} for {repo}",
        ],
        cwd=monorepo.project_folder,
    )


def is_synchronized_commits_file_existing(
    monorepo: GitMonorepoConfig,
    repo: Optional[str] = None,
) -> bool:
    sync_file_path = os.path.join(monorepo.project_folder, MONOREPO_SYNC_FILE)
    is_file = os.path.isfile(sync_file_path)

    if not is_file:
        return False

    if not repo:
        return True

    with open(sync_file_path, "rt", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        return repo in data


def _read_synchronized_commits(project_folder: str) -> Dict[str, List[str]]:
    sync_file_name = os.path.join(project_folder, MONOREPO_SYNC_FILE)

    if not os.path.isfile(sync_file_name):
        return dict()

    with open(sync_file_name, "rt", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _merge_repos(*, repos: Dict[str, str], path: str, data: Dict[str, Any]) -> None:
    for key_name, key_value in data.items():
        relative_path = os.path.join(path, key_name)

        if isinstance(key_value, str):
            repos[relative_path] = key_value
            continue

        _merge_repos(
            repos=repos,
            path=relative_path,
            data=key_value,
        )


def _create_synchronized_commits(
    monorepo: GitMonorepoConfig,
) -> Dict[str, List[str]]:
    result = dict()
    current_commit = get_current_commit(project_folder=monorepo.project_folder)

    for repo_folder in monorepo.repos:
        result[repo_folder] = [current_commit]

    return result


def get_current_commit(*, project_folder: str) -> str:
    return (
        subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=project_folder,
        )
        .decode("utf-8")
        .strip()
    )


def _resolve_in_repo(monorepo: GitMonorepoConfig, path: str) -> str:
    """
    Resolves a path inside the monorepo, to allow working inside folders
    """
    absolute_path = os.path.abspath(path)

    if not absolute_path.startswith(monorepo.project_folder):
        print(
            red(path, bold=True),
            red("resolved to"),
            red(absolute_path, bold=True),
            red("was not in the project folder:"),
            red(monorepo.project_folder, bold=True),
        )
        sys.exit(1)

    return os.path.relpath(absolute_path, monorepo.project_folder)
