import os
import tempfile
import shutil
import errno


def create_temp_folder():
    temp_folder = tempfile.mkdtemp(prefix='germanium_', suffix='install')

    def temp(subpath=''):
        return os.path.join(temp_folder, subpath)

    return temp


def get_germanium_folder(germanium_home):
    def ge_folder(subpath=''):
        return os.path.join(germanium_home, subpath)

    return ge_folder


def get_desktop_folder():
    home_folder = os.environ['USERPROFILE']

    def desktop_folder(subpath=''):
        return os.path.join(home_folder, 'Desktop', subpath)

    return desktop_folder


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm_rf(*paths):
    for path in paths:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        elif os.path.exists(path):
            os.remove(path)


def create_desktop_link(title, application, icon=None, workdir=None):
    desktop_folder = get_desktop_folder()

    if not icon:
        icon = application

    if not workdir:
        workdir = os.path.dirname(application)

    path = desktop_folder("%s.lnk" % title)

    try:
        from win32com.client import Dispatch

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = application
        shortcut.WorkingDirectory = workdir
        shortcut.IconLocation = icon
        shortcut.save()
    except ImportError as e:
        pass
