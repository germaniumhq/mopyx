
import threading

global_germanium = threading.local()
global_germanium._instance = None


def get_instance():
    """
    :return: GermaniumDriver
    """
    global global_germanium

    return global_germanium._instance


def set_instance(instance):
    global global_germanium

    global_germanium._instance = instance
