from selenium.webdriver.remote.webelement import WebElement

from germanium.impl import _filter_not_displayed, _is_displayed_filter
from .find_germanium_object import find_germanium_object


def highlight_g(context,
                selector,
                show_seconds=2,
                *args,
                console=False,
                blink_duration=0.2,
                **kw):
    """
    Highlight the given element, by blinking it on the UI.
    :param context:
    :param selector:
    :param show_seconds:
    :param args:
    :param console:
    :param blink_duration:
    :param kw:
    :return:
    """
    germanium = find_germanium_object(context)

    if isinstance(selector, WebElement):
        element = selector
        is_element_visible = _is_displayed_filter(element)
    else:
        items = germanium.S(selector).element_list(only_visible=False)
        is_element_visible = True
        elements = _filter_not_displayed(germanium, items, throw_when_empty=False)

        if not elements:
            elements = items
            is_element_visible = False

        if elements:
            element = elements[0]
        else:
            element = None

    if not element:
        message = "GERMANIUM: Unable to find element with selector `%s`." % selector
        if console:
            germanium.js("console.error(arguments[0]);",
                         message)
        else:
            germanium.js("""
                var message = arguments[0];
                setTimeout(function() {
                    alert(message);
                });
            """, message)

        return  # ==> not element

    if not is_element_visible:
        message = "GERMANIUM: Element with selector `%s` was found, but is not visible." % selector
        if console:
            germanium.js("console.error(arguments[0], arguments[1]);",
                         message,
                         element)
        else:
            germanium.js("""
                var message = arguments[0];
                setTimeout(function() {
                    alert(message);
                });
            """, message)

        return  # ==> not is_element_visible

    if console:
        message = "GERMANIUM: Element with selector `%s` was found." % selector
        germanium.js("console.log(arguments[0], arguments[1]);",
                     message,
                     element)

    code = """
        if (window._germaniumCurrentHighlight) {
            return;
        }

        window._germaniumCurrentHighlight = arguments[0];

        var element = arguments[0];
        var index = %d;
        var originalOutline = element.style.outline;

        element.style.outline = '#00ff00 2px solid';

        var interval = setInterval(function() {
            index--;

            if (index %% 2 == 1) {
                element.style.outline = '#00ff00 2px solid';
            } else {
                element.style.outline = originalOutline;
            }

            if (index == 0) {
                window._germaniumCurrentHighlight = undefined;
                try {
                    delete window._germaniumCurrentHighlight;
                } catch(e) {}
                clearInterval(interval);
            }
        }, %d);
    """ % (round(show_seconds / blink_duration), int(blink_duration * 1000))

    germanium.js(code, element)
