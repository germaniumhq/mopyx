#!/usr/bin/env python

import sys

install_requires = []
with open("requirements.txt", mode="r") as requirements_file:
    for line in requirements_file.readlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.endswith("# optional"):
            install_requires.append('"%s"' % line.strip())

if not install_requires:
    sys.exit(0)

if len(install_requires) == 1:
    print(install_requires[0])
    sys.exit(0)

print("\n        " + ",\n        ".join(install_requires) + ",\n    ")
