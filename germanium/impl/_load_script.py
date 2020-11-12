import pkg_resources


def load_script(package_name, script_name):
    code = pkg_resources.resource_string(package_name, script_name)
    if type(code) != 'str':  # it is bytes
        code = code.decode('utf-8')

    return code
