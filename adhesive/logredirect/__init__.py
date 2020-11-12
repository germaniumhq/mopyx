from adhesive import config


def is_enabled():
    return not config.current.boolean.stdout
