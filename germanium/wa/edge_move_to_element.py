def _is_microsoft_edge(germanium):
    capabilities = germanium.web_driver.capabilities
    return capabilities['browserName'].lower() == 'microsoftedge'


def _edge_move_to_element_with_offset(germanium, original_function, *args, **kw):
    action = args[1]
    element = args[2]
    return action.move_to_element_with_offset(element, 0, 0)
