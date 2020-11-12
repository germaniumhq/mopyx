from behave import *

from germanium.static import *

use_step_matcher("re")


@step("I get the parent node of the element with id 'childDiv'")
def find_parent_node(context):
    context.found_element = parent_node('#childDiv')
