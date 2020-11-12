import os
import pkg_resources
import stat

try:
    import urllib.request as urllib2  # type: ignore
except ImportError:
    import urllib2  # type: ignore

from . import driver_registry
from .driver_registry import get_internal_driver_path, is_driver_up_to_date
from .configurable_settings import get_germanium_drivers_folder, is_ms_edge_license_agreed


def install_driver(platform, browser):
    """
    Installs the driver into a new folder that will also be added into the path.
    :param platform:
    :param browser:
    :return:
    """
    driver_name = driver_registry.get_driver_name(platform, browser)

    if not driver_name:
        raise Exception("Unsupported Platform/Browser combination. '%s', "
                        "browser: '%s'." % (platform, browser))

    drivers_folder = get_germanium_drivers_folder()

    if os.path.exists(drivers_folder):
        if not os.path.isdir(drivers_folder):
            raise Exception("The drivers folder %s, exists already but is not a file. "
                            "Please specify a different location using the "
                            "GERMANIUM_DRIVERS_FOLDER environment variable." % drivers_folder)
    else:
        os.makedirs(drivers_folder)

    path_folders = os.environ['PATH'].split(os.pathsep)
    path_folders.insert(0, drivers_folder)
    os.environ['PATH'] = os.pathsep.join(path_folders)

    full_path_to_driver = os.path.join(drivers_folder, driver_name)

    if driver_registry.is_driver_up_to_date(platform, browser, full_path_to_driver):
        return full_path_to_driver

    internal_driver_path = get_internal_driver_path(platform, browser)
    data = load_data(internal_driver_path)

    # if the driver already exists, we're going to try to remove it first, otherwise
    # Java complains.
    if os.path.exists(full_path_to_driver):
        os.remove(full_path_to_driver)

    new_file = open(full_path_to_driver, 'wb')
    new_file.write(data)
    new_file.close()

    if platform.operating_system == "linux" or platform.operating_system == "mac":
        new_file_stat = os.stat(full_path_to_driver)
        os.chmod(full_path_to_driver, new_file_stat.st_mode | stat.S_IEXEC)

    return full_path_to_driver


def load_data(path_or_url):
    """
    Loads the bytes for from the internal resource, or the given URL
    """
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"): #  url
        validate_license_agreement()
        data = urllib2.urlopen(path_or_url).read()
    else:
        data = pkg_resources.resource_stream(__name__, path_or_url).read()

    return data


def validate_license_agreement():
    if is_ms_edge_license_agreed():
        return

    raise Exception("In order to use Edge, you need to first read the EULA from "
                    "https://az813057.vo.msecnd.net/eulas/webdriver-eula.pdf . If "
                    "you agree with it, you can either: 1. export GERMANIUM_I_AGREE_TO_MS_EDGE_LICENSE "
                    "into the environment, or 2. call germaniumdrivers.i_agree_to_ms_edge_license(). "
                    "Afterwards Germanium will download the drivers for you automatically. By default the "
                    "download will be in a temporary file, but you can configure the location using the "
                    "GERMANIUM_DRIVERS_FOLDER environment variable.")
