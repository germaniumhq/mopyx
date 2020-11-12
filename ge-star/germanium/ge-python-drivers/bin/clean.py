#!/usr/bin/env python

import shutil
import os.path


PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))


def project_remove(path):
    print("Removing: %s" % path)
    shutil.rmtree(os.path.join(PROJECT_DIR, path), ignore_errors=True)


project_remove('dist')
project_remove('build')
project_remove('germaniumdrivers.egg-info')
