import os.path


def display_project_location(projects_folder: str, project_name: str) -> None:
    print(os.path.join(projects_folder, project_name))
