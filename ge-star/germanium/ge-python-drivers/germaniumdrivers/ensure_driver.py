import platform
import sys

from .available_driver import get_available_driver_from_path
from .configurable_settings import is_germanium_use_path_driver_set
from .driver_registry import is_driver_up_to_date
from .install_driver import install_driver


def ensure_driver(browser):
    """
    Ensures that the WebDriver is correctly installed.
    :param browser:
    :return:
    """
    current_platform = detect_platform()

    found_driver = get_available_driver_from_path(current_platform, browser)

    if not found_driver:
        return install_driver(current_platform, browser)

    if is_driver_up_to_date(current_platform, browser, found_driver):
        return found_driver.path

    # There is a driver, but not the Germanium approved one, either the user
    # forces us to use it, or we install the new driver ourselves.
    if is_germanium_use_path_driver_set():
        print("Germanium found a driver at `%s`. Unfortunately this is not matching "
              "the current version embedded in Germanium, but since Germanium was "
              "configured via GERMANIUM_USE_PATH_DRIVER to use this one in the path, "
              "it will not use the embedded one. If you want to configure Germanium "
              "to use the embedded driver then please unset the "
              "GERMANIUM_USE_PATH_DRIVER environment variable. Note that Germanium "
              "support is only offered for the embedded drivers." % found_driver.path)
        return found_driver.path

    print("Germanium found a driver at `%s`. Unfortunately this is not matching "
          "the current version embedded in Germanium, so Germanium will use the "
          "embedded one. If you want to force Germanium to use the driver from "
          "the PATH, then you can set the GERMANIUM_USE_PATH_DRIVER environment "
          "variable. Note that Germanium support is only offered for the embedded "
          "drivers." % found_driver.path)

    return install_driver(current_platform, browser)


def detect_platform():
    bits = "64" if platform.machine().endswith("64") else "32"
    if sys.platform.startswith("linux"):
        operating_system = "linux"
    elif sys.platform.startswith("win"):
        operating_system = "win"
    elif sys.platform.startswith("darwin"):
        operating_system = "mac"
    else:
        raise "Unsupported platform: %s. Only linux, win and mac are supported." % sys.platform

    return Platform(operating_system, bits)


class Platform(object):
    def __init__(self, operating_system, bits):
        self.operating_system = operating_system
        self.bits = bits

    def __str__(self):
        """ toString """
        return "Platform: %s bit %s" % (self.bits, self.operating_system)
