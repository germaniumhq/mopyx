#!/usr/bin/env python

install_requires = []
with open("requirements.txt", mode="r") as requirements_file:
    for line in requirements_file.readlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.endswith("# optional"):
            install_requires.append('        "%s",' % line.strip())

print("\n" + "\n".join(install_requires) + "\n    ")
