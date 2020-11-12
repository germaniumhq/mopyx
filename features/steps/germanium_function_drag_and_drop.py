from behave import *
from germanium.static import *

from features.steps.asserts import *


@step(u'I drag and drop from the #startDiv to the #endDiv')
def i_drag_and_drop_from_start_to_end(context):
    drag_and_drop('#startDiv', '#endDiv')


@step(u'the drag and drop events correspond')
def check_drag_and_drop_events(context):
    assert_equals("startDiv mousedown\nendDiv mouseup",
                  Css('#messages').text(only_visible=False).strip())
