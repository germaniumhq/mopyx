from behave import *
from selenium.webdriver.remote.webelement import WebElement

from germanium.static import *

use_step_matcher("re")


@step("I get the child nodes for the element '(.*?)'")
def find_child_nodes(context, node_id):
    context.found_element_list = child_nodes('#' + node_id, only_elements=False)


@step("I get only the child elements for the element '(.*?)'")
def find_child_elements_only(context, node_id):
    context.found_element_list = child_nodes('#' + node_id)


@step(r"I get 5 child nodes: 3 text nodes, a div \(#childDiv\) and a span \(#childSpan\)")
def check_if_we_have_5_child_nodes(context):
    assert len(context.found_element_list) == 5
    assert isinstance(context.found_element_list[1], WebElement)
    assert "div" == context.found_element_list[1].tag_name
    assert isinstance(context.found_element_list[3], WebElement)
    assert "span" == context.found_element_list[3].tag_name


@step("I get back an empty list as child nodes")
def check_if_we_have_an_empty_list_of_nodes(context):
    assert isinstance(context.found_element_list, list)
    assert len(context.found_element_list) == 0


@step(r"I get 2 child nodes: a div \(#childDiv\) and a span \(#childSpan\)")
def check_if_we_have_2_child_nodes(context):
    assert len(context.found_element_list) == 2
    assert isinstance(context.found_element_list[0], WebElement)
    assert "div" == context.found_element_list[0].tag_name
    assert isinstance(context.found_element_list[1], WebElement)
    assert "span" == context.found_element_list[1].tag_name
