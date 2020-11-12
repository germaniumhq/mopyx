
from germanium.selectors import *
from germanium.points import *
from germanium.impl import wait, waited
from germanium.util import Color

# germanium instantiation
from .open_browser import open_browser
from .close_browser import close_browser
from .get_germanium import get_germanium
from .get_web_driver import get_web_driver

# germanium instance functions
from .click import click
from .double_click import double_click
from .go_to import go_to
from .hover import hover
from .right_click import right_click
from .S import S
from .type_keys import type_keys
from .js import js
from .get_attributes import get_attributes
from .drag_and_drop import drag_and_drop
from .select import select
from .deselect import deselect
from .select_file import select_file

from .parent_node import parent_node
from .child_nodes import child_nodes
from .get_value import get_value
from .get_text import get_text
from .get_style import get_style
from .highlight import highlight

from .use_window import use_window

# decorators
from .iframe import iframe
