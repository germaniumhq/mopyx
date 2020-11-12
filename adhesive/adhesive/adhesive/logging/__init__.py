import logging
import sys


def configure_logging(config) -> None:
    debug_levels = {
        "trace": 5,                    # 5
        "debug": logging.DEBUG,        # 10
        "info": logging.INFO,          # 20
        "warning": logging.WARNING,    # 30
        "error": logging.ERROR,        # 40
        "critical": logging.CRITICAL,  # 50
    }

    if config.log_level not in debug_levels:
        raise Exception(
            f"Log level {config.log_level} not in the available log levels: "
            f"{debug_levels.keys()}")

    logging.basicConfig(
            level=debug_levels[config.log_level],
            stream=sys.stdout,
            format='%(asctime)-15s %(levelname)-8s %(message)s')

