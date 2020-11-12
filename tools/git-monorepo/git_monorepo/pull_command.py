import os
import subprocess
import sys
from typing import List

from termcolor_util import yellow, red, green

from git_monorepo.git_monorepo_config import (
    read_monorepo_config,
    get_current_commit,
    write_synchronized_commits,
    is_synchronized_commits_file_existing,
    _resolve_in_repo,
    GitMonorepoConfig,
)
from git_monorepo.git_util import env_extend, is_repo_unchanged


def pull(
    sync: bool,
    folders: List[str],
    required: bool = False,
) -> None:
    validate_flags(folders, required)
    monorepo = read_monorepo_config()

    folders = get_folders_to_update(monorepo, folders, required)
    validate_folders_to_update(monorepo, folders, required)

    for folder_name, repo_location in monorepo.repos.items():
        if folders and not folder_name in folders:
            continue

        absolute_folder_name = os.path.join(monorepo.project_folder, folder_name)

        print(
            yellow(repo_location, bold=True),
            yellow("->"),
            yellow(absolute_folder_name, bold=True),
        )

        initial_commit = get_current_commit(project_folder=monorepo.project_folder)

        try:
            if not os.path.isdir(absolute_folder_name):
                add_monorepo_project(monorepo, folder_name, repo_location)
            else:
                pull_monorepo_project(monorepo, folder_name, repo_location)
        except Exception as e:
            # FIXME: we assume blindly atm this is a merge issue
            patch_commit_message(monorepo, folder_name, "COMMIT_EDITMSG")
            patch_commit_message(monorepo, folder_name, "MERGE_MSG")
            raise e

        current_commit = get_current_commit(project_folder=monorepo.project_folder)

        if current_commit == initial_commit and is_synchronized_commits_file_existing(
            monorepo, repo=folder_name
        ):
            continue

        if not sync:
            print(yellow("Not syncing as requested"))
            continue

        write_synchronized_commits(monorepo, repo=folder_name, commit=current_commit)


def pull_monorepo_project(
    monorepo: GitMonorepoConfig, folder_name: str, repo_location: str
) -> None:
    pull_command = [
        "git",
        "subtree",
        "pull",
        "-P",
        folder_name,
        repo_location,
        monorepo.current_branch,
    ]

    if monorepo.squash:
        pull_command.insert(3, "--squash")

    subprocess.check_call(
        pull_command,
        cwd=monorepo.project_folder,
        env=env_extend(
            {
                "EDITOR": "git-monorepo-editor",
                "GIT_MONOREPO_EDITOR_MESSAGE": f"git-monorepo: Sync {folder_name}",
            }
        ),
    )


def add_monorepo_project(
    monorepo: GitMonorepoConfig, folder_name: str, repo_location: str
) -> None:
    add_command = [
        "git",
        "subtree",
        "add",
        "-P",
        folder_name,
        repo_location,
        monorepo.current_branch,
    ]

    if monorepo.squash:
        add_command.insert(3, "--squash")

    subprocess.check_call(
        add_command,
        cwd=monorepo.project_folder,
        env=env_extend(
            {
                "EDITOR": "git-monorepo-editor",
                "GIT_MONOREPO_EDITOR_MESSAGE": f"git-monorepo: Sync {folder_name}",
            }
        ),
    )


def validate_folders_to_update(
    monorepo: GitMonorepoConfig, folders: List[str], required: bool
) -> None:
    pull_folders = set(folders)
    pull_folders.difference_update(monorepo.repos)
    if pull_folders:
        print(
            red("Error:"),
            red(", ".join(pull_folders), bold=True),
            red("not found in monorepo projects."),
        )
        sys.exit(1)

    if not folders and required:
        print(green("Nothing changed locally.", bold=True), green("Nothing to do."))
        sys.exit(0)


def get_folders_to_update(
    monorepo: GitMonorepoConfig, folders: List[str], required: bool
) -> List[str]:
    if required:
        folders = [it for it in monorepo.repos if not is_repo_unchanged(monorepo, it)]
    else:
        # we normalize relative paths, extra slashes, etc
        folders = [_resolve_in_repo(monorepo, it) for it in folders]
    return folders


def validate_flags(folders: List[str], required: bool) -> None:
    if required and folders:
        print(
            red("You can't specify both"),
            red("--required", bold=True),
            red("and"),
            red("folders", bold=True),
        )
        sys.exit(1)


def patch_commit_message(
    monorepo: GitMonorepoConfig, folder_name: str, message_file: str
) -> None:
    commit_message_file = os.path.join(monorepo.project_folder, ".git", message_file)
    if not os.path.isfile(commit_message_file):
        return

    message = f"git-monorepo: Sync conflict {folder_name}"

    with open(commit_message_file, "rt", encoding="utf-8") as f:
        commit_file_content = f.read()

    with open(commit_message_file, "wt", encoding="utf-8") as f:
        f.write(message)
        f.write("\n")
        f.write(commit_file_content)
