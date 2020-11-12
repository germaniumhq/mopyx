from behave import *
from germanium.static import *

use_step_matcher("re")


@step(u'I look for a custom button selector with the text: \'(.*?)\'')
def step_impl(context, expected_text):
    selector = AnyOfSelector(
        Element("button", exact_text=expected_text),
        Element("input", exact_attributes={"type": "button", "value": expected_text}),
        Element("input", exact_attributes={"type": "submit", "value": expected_text}),
    )

    element = S(selector).element()

    context.found_element = element
