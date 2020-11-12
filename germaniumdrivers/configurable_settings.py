import tempfile
import os


_ms_edge_license_agreed = False


def is_germanium_use_ie_driver_for_platform():
    return 'GERMANIUM_USE_IE_DRIVER_FOR_PLATFORM' in os.environ


def is_germanium_use_path_driver_set():
    return 'GERMANIUM_USE_PATH_DRIVER' in os.environ


def get_germanium_drivers_folder():
    if 'GERMANIUM_DRIVERS_FOLDER' not in os.environ:
        return os.path.join(tempfile.gettempdir(), 'germanium-drivers')

    return os.environ['GERMANIUM_DRIVERS_FOLDER']


def is_ms_edge_license_agreed():
    return _ms_edge_license_agreed or 'GERMANIUM_I_AGREE_TO_MS_EDGE_LICENSE' in os.environ


def i_agree_to_ms_edge_license():
    global _ms_edge_license_agreed
    _ms_edge_license_agreed = True
