import subprocess
import os
import sys
from textwrap import dedent
from PySide2.QtWidgets import QWidget, QMessageBox


def base_dir(sub_path=""):
    # pth is set by pyinstaller with the folder where the application
    # will be unpacked.
    if 'pth' in globals():
        return os.path.join(pth, sub_path)  # NOQA

    return os.path.abspath(os.path.dirname(__file__))


def help_show() -> None:
    if sys.platform.startswith("win"):
        documentation_path = os.path.abspath(
            os.path.join(
                base_dir("germaniumsb"), "doc", "index.chm"))
        subprocess.check_call(['hh.exe', documentation_path])

        return

    documentation_path = os.path.abspath(
        os.path.join(
            base_dir("germaniumsb"), "doc", "index.html"))
    subprocess.check_call(['xdg-open', documentation_path])


def help_about_qt(parent: QWidget) -> None:
    QMessageBox.aboutQt(parent, "Felix Build Monitor v1.0.0")


def help_about(parent: QWidget) -> None:
    QMessageBox.about(parent,
                      "Felix Build Monitor v1.0.0",
                      dedent("""\
                          Released under license AGPL v3.

                          (c) 2017-2018 Germanium HQ e.U. All rights reserved.

                          Icons created by Nishat Tasnim Onu <nishattasnimonu@gmail.com>.

                          Made with passion in Austria.
                      """))

