from typing import List, Set
import re
import os


class FileEntry(object):
    name: str
    absolute_path: str
    owning_project: str
    is_dir: bool
    is_exe: bool

    def __init__(
        self,
        name: str,
        absolute_path: str,
        owning_project: str,
        is_dir: bool,
        is_exe: bool,
    ) -> None:
        self.name = name
        self.absolute_path = absolute_path
        self.owning_project = owning_project
        self.is_dir = is_dir
        self.is_exe = is_exe


class FileResolver(object):
    def __init__(
        self, root_projects_folder: str, search_path: List[str], current_path: str = "."
    ) -> None:
        self.root_projects_folder = root_projects_folder
        self.search_path = list(search_path)
        self.current_path = current_path

    def listdir(self) -> List[FileEntry]:
        """
        Lists the current folder, by iterating the search path that
        was provided and aggregating all the files from there.
        """
        current_files: Set[str] = set()
        result: List[FileEntry] = list()

        for searched_folder in self.search_path:
            abs_path = os.path.join(
                self.root_projects_folder, searched_folder, self.current_path
            )

            if not os.path.isdir(abs_path):
                continue

            for found_entry in os.listdir(abs_path):
                local_entry = name_without_flags(found_entry)

                if local_entry in current_files:
                    continue

                current_files.add(local_entry)

                abs_entry = os.path.join(abs_path, found_entry)

                result.append(
                    FileEntry(
                        name=found_entry,
                        owning_project=searched_folder,
                        absolute_path=abs_entry,
                        is_dir=os.path.isdir(abs_entry),
                        is_exe=os.access(abs_entry, os.X_OK),
                    )
                )

        result.sort(key=lambda it: (not it.is_dir, it.name.lower()))
        return result

    def subentry(self, entry: FileEntry = None, path: str = None) -> "FileResolver":
        if not entry and not path:
            raise Exception("You need to pass an entry or a subpath")

        sub_path = ""

        if path:
            sub_path = path

        if entry:
            sub_path = entry.name

        return FileResolver(
            root_projects_folder=self.root_projects_folder,
            search_path=self.search_path,
            current_path=os.path.join(self.current_path, sub_path),
        )


NAME_EXTRACTOR = re.compile(r"(.*?)(\.hbs)?(\.KEEP)?$")


def name_without_flags(name: str) -> str:
    m = NAME_EXTRACTOR.match(name)
    assert m

    return m.group(1)


def is_first_file_newer(first_file: str, second_file: str) -> bool:
    """
    Checks if the last modification date of the first file
    is after the modification date of the second file.
    """
    first_file_time = os.path.getmtime(first_file)
    second_file_time = os.path.getmtime(second_file)

    return first_file_time >= second_file_time
