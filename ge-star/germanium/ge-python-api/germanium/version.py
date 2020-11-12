
current = "2.0.11"


def display_version():
    print('                                          _')
    print('   ____ ____  _________ ___  ____ _____  (_)_  ______ ___')
    print('  / __ `/ _ \/ ___/ __ `__ \/ __ `/ __ \/ / / / / __ `__ \\')
    print(' / /_/ /  __/ /  / / / / / / /_/ / / / / / /_/ / / / / / /')
    print(' \__, /\___/_/  /_/ /_/ /_/\__,_/_/ /_/_/\__,_/_/ /_/ /_/')
    print('/____/ %s' % current)


def display_simple_version():
    print("Germanium %s" % current)


if __name__ == "__main__":
    display_version()
