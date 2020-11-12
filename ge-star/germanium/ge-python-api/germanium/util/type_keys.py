import re
import time

from selenium.webdriver.common.keys import Keys

from germanium.impl import ActionChains
from germanium.impl import _filter_one_for_action
from .find_germanium_object import find_germanium_object

MULTIPLE_TIMES_KEY_PRESS_RE = re.compile("^(.*?)\*(\d+)$")


class BasicKeysAction(object):
    """
    A class that just denotes basic keys to be sent to the WebDriver.
    basic keys can also be made of keys such as ENTER, UP, etc.
    """
    def __init__(self, keys):
        self.keys = []
        for i in range(len(keys)):
            self.keys.append(keys[i])


class ComboKeyDown(object):
    """
    An action that marks a single combo key that should be pressed
    !shift, !control, !ctrl, !alt
    """
    def __init__(self, key):
        self.key = key


class ComboKeyUp(object):
    """
    An action that marks a single combo key that should be released
    ^shift, ^control, ^ctrl, ^alt
    """
    def __init__(self, key):
        self.key = key


def type_keys_g(context, keys_typed, selector=None, delay=0, *args):
    """
    :param context:
    :param keys_typed:
    :param selector:
    :param delay:
    :param args:
    """
    germanium = find_germanium_object(context)
    keys_array = transform_to_keys(keys_typed)
    element = None

    if selector:
        potential_elements = germanium.S(selector).element_list(only_visible=False)
        element = _filter_one_for_action(germanium, potential_elements)

    action_chain = ActionChains(germanium.web_driver)

    # We don't just randomly start sending keys, but we click first
    # the element so it has focus, then only start typing in case the
    # element is not focused.
    if selector and element and \
            germanium.js('return arguments[0] != document.activeElement;', element):
        action_chain.click(on_element=element)
        action_chain.add_action(lambda: time.sleep(0.2))  # wait for the selection to settle

    # In case we have delays, we will pass insert after each character a small delay.
    # This is factored in different functions, since otherwise there would be way
    # to much ifing to add the delays.
    # The ActionChains used is extended from the WebDriver one so we can also add
    # custom callables into the action chain.
    if delay:
        add_delayed_keys(action_chain, keys_array, element, delay)
    else:
        add_immediate_keys(action_chain, keys_array, element)

    action_chain.perform()


def add_immediate_keys(action_chain, keys_array, element):
    for key_action in keys_array:
        if isinstance(key_action, BasicKeysAction):
            keys_to_send = ''.join(key_action.keys)
            if element:
                action_chain.send_keys_to_element(element, keys_to_send)
            else:
                action_chain.send_keys(keys_to_send)
        elif isinstance(key_action, ComboKeyDown):
            action_chain.key_down(key_action.key, element)
        elif isinstance(key_action, ComboKeyUp):
            action_chain.key_up(key_action.key, element)


def add_delayed_keys(action_chain, keys_array, element, delay):
    for key_action in keys_array:
        if isinstance(key_action, BasicKeysAction):
            if element:
                for key in key_action.keys:
                    action_chain.send_keys_to_element(element, key)
                    action_chain.add_action(lambda: time.sleep(delay))
            else:
                for key in key_action.keys:
                    action_chain.send_keys(key)
                    action_chain.add_action(lambda: time.sleep(delay))
        elif isinstance(key_action, ComboKeyDown):
            action_chain.key_down(key_action.key, element)
            action_chain.add_action(lambda: time.sleep(delay))
        elif isinstance(key_action, ComboKeyUp):
            action_chain.key_up(key_action.key, element)
            action_chain.add_action(lambda: time.sleep(delay))


def transform_to_keys(keys):
    """
    Transforms the given keys string into an array of keys action
    that can be fed into an ActionChain
    """
    combo_re = re.compile('<(.*?)>')
    combo_key_scanner = combo_re.scanner(keys)

    initial_key_index = 0
    transformed_keys = []
    last_action = None

    while True:
        m = combo_key_scanner.search()
        if not m:
            break

        if m.start() - initial_key_index > 0:
            if isinstance(last_action, BasicKeysAction):
                for key in keys[initial_key_index: m.start()]:
                    last_action.keys.append(key)
            else:
                action = BasicKeysAction(keys[initial_key_index: m.start()])
                last_action = action
                transformed_keys.append(action)

        pressed_keys = m.group(1)

        if is_up_down_toggle(pressed_keys):
            action = create_up_down_toggle(pressed_keys)
            transformed_keys.append(action)
            last_action = action
        elif is_multikey_combo(pressed_keys):
            multi_combo_actions = create_multicombo(pressed_keys)
            for multi_combo_action in multi_combo_actions:
                transformed_keys.append(multi_combo_action)
                last_action = multi_combo_action
        else:
            if isinstance(last_action, BasicKeysAction):
                key = create_custom_key(pressed_keys)

                for i in range(get_keypress_count(pressed_keys)):
                    last_action.keys.append(key)
            else:
                multiple_keys = []
                key = create_custom_key(pressed_keys)

                kp = get_keypress_count(pressed_keys)

                for i in range(kp):
                    multiple_keys.append(key)

                action = BasicKeysAction(multiple_keys)
                transformed_keys.append(action)

        initial_key_index = m.end()

    if len(keys) - initial_key_index > 0:
        action = BasicKeysAction(keys[initial_key_index:])
        transformed_keys.append(action)

    return transformed_keys


def is_multikey_combo(pressed_keys):
    return "-" in pressed_keys


def is_up_down_toggle(pressed_keys):
    return pressed_keys.find('^') == 0 or \
           pressed_keys.find('!') == 0


def create_up_down_toggle(pressed_keys):
    """
    Create a toggling of a button down.
    :param pressed_keys:
    :return:
    """
    if pressed_keys.find('^') == 0:  # release key
        key = create_custom_key(pressed_keys[1:])

        if get_keypress_count(pressed_keys[1:]) != 1:
            raise Exception("The key can be released only once.")

        return ComboKeyUp(key)
    elif pressed_keys.find('!') == 0:  # pressed key
        key = create_custom_key(pressed_keys[1:])

        if get_keypress_count(pressed_keys[1:]) != 1:
            raise Exception("The key can be pressed only once.")

        return ComboKeyDown(key)
    else:
        raise Exception("Unable to create key toggle for: '%s'" % pressed_keys)


def create_multicombo(pressed_keys):
    """
    Create a combo made of multiple keys (e.g. ctrl-shift-s)
    :param pressed_keys:
    :return:
    """
    result = []
    combo_key=None

    tokens = pressed_keys.split("-")
    keypress_count = 1

    for i in reversed(range(len(tokens))):
        if i < len(tokens) - 1:
            custom_key = create_custom_key(tokens[i])
            combo_key = custom_key + combo_key + custom_key
        else:
            combo_key = create_key(tokens[i])
            keypress_count = get_keypress_count(tokens[i])

    for i in range(keypress_count):
        result.append(BasicKeysAction(combo_key))

    return result


def create_custom_key(combo_string):
    """
    Create a single key for webdriver that represents a custom
    key (<CR>, <SHIFT>, <UP> etc)
    """

    m = MULTIPLE_TIMES_KEY_PRESS_RE.match(combo_string)
    if m:
        combo_string = m.group(1)

    key_string = combo_string.upper()

    key = create_abbreviated_key(key_string)
    if key:
        return key

    if key_string == "C":
        return Keys.CONTROL
    elif key_string == "S":
        return Keys.SHIFT
    elif key_string == "M":
        return Keys.META

    return getattr(Keys, key_string)


def create_key(combo_string):
    """
    Create a single key for webdriver that represents a regular
    or a custom key, that is the last part of the macro.
    """
    # if it's a single character return it
    if len(combo_string) <= 1:
        return combo_string

    m = MULTIPLE_TIMES_KEY_PRESS_RE.match(combo_string)
    if (m):
        combo_string = m.group(1)

    key_string = combo_string.upper()
    key = create_abbreviated_key(key_string)

    if key:
        return key

    return getattr(Keys, key_string)


def get_keypress_count(combo_string):
    """
    Finds the number of times a key is pressed:
    `c` - once
    `c*3` - three times
    """
    m = MULTIPLE_TIMES_KEY_PRESS_RE.match(combo_string)

    if (m):
        result = int(m.group(2))
        if result <= 0:
            raise Exception("The number of key presses should be more than 0.");
        return result

    return 1

def create_abbreviated_key(key_string):
    if key_string == "CR":
        return Keys.ENTER
    elif key_string == "CTRL" or \
         key_string == "CTL":
        return Keys.CONTROL
    elif key_string == "DEL":
        return Keys.DELETE
    elif key_string == "CMD":
        return Keys.COMMAND
    elif key_string == "BS":
        return Keys.BACKSPACE
    elif key_string == "INS":
        return Keys.INSERT
    elif key_string == "PGUP":
        return Keys.PAGE_UP
    elif key_string == "PGDN":
        return Keys.PAGE_DOWN

    return None
