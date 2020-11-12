#!/usr/bin/env python

install_requires = []
with open('requirements.txt', mode='r') as requirements_file:
    for line in requirements_file.readlines():
        if line and not line.startswith('#'):
            install_requires.append('        "%s"' % line.strip())

print("\n" + ",\n".join(install_requires))
