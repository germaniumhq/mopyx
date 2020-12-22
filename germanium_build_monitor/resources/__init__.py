import os


def base_dir(sub_path="germanium_build_monitor/resources"):
    # pth is set by pyinstaller with the folder where the application
    # will be unpacked.
    if 'pth' in globals():
        return os.path.join(pth, sub_path)  # NOQA

    return os.path.abspath(os.path.dirname(__file__))

