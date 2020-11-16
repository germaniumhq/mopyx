#!/usr/bin/env python

import shutil
import os
import re


EXTENSION_EXTRACTOR_RE = re.compile(r"^(.*\/)?(.+?)(\.([^\.]+))?$")
PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))


def extension(filename: str) -> str:
    m = EXTENSION_EXTRACTOR_RE.match(filename)

    if not m:
        return ""

    return m.group(3)


def project_remove(path):
    print("Removing: %s" % path)
    shutil.rmtree(os.path.join(PROJECT_DIR, path), ignore_errors=True)


def remove_single_file(path):
    print("Removing file: %s" % path)
    os.remove(path)


project_remove("dist")
project_remove("build")
project_remove("weary.egg-info")

for f, folders, files in os.walk("."):
    if os.path.basename(f) in ["__pycache__", ".mypy_cache"]:
        project_remove(f)
        continue

    for file_name in files:
        if extension(file_name) in [".orig", ".pyc"]:
            remove_single_file(os.path.join(f, file_name))
