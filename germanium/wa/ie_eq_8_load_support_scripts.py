def _is_ie_8(germanium):
    capabilities = germanium.web_driver.capabilities
    return capabilities['browserName'] == 'internet explorer' and \
           capabilities['version'] == '8'


def _ie_8_load_support_scripts(germanium, original_function, *args, **kw):
    """
    Since the support scripts are quite big, they should be loaded independently.
    """
    if germanium.js("return !window.__GERMANIUM_EXTENSIONS_LOADED"):
        germanium.load_script('germanium-ie8-getComputedStyle.js')

        for script_name in germanium._scripts_to_load:
            germanium.load_script(script_name)

        germanium.load_script('germanium-extensions-loaded.js')
