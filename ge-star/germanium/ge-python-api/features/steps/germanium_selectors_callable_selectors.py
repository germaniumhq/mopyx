from behave import *
from germanium.static import *

from features.steps.asserts import *

use_step_matcher("re")


@step(u'I search for a div element using the InputText class as parameter')
def step_impl(context):
    selector = Element("div", id="inputTextContainer").containing(InputText)
    element = selector.element()

    assert element

    context.found_element = element
