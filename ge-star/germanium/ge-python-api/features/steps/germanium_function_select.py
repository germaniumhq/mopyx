from behave import *

from germanium.static import *
from features.steps.asserts import *

use_step_matcher("re")


@step(u"I select in the first select the entry with text 'A1'")
def step_impl(context):
    select("#firstSelect", "A1")


@step(u"I select in the multiline select the entries with texts B1 and B4")
def step_impl(context):
    select("#multilineSelect", ["B1", "B4"])


@step(u"I select in the first select the entry with value 'a2value'")
def step_impl(context):
    select("#firstSelect", value="a2value")


@step(u"I select in the multiline select the entries with values b2value, b4value and b6value")
def step_impl(context):
    select("#multilineSelect", value=["b2value", "b4value", "b6value"])


@step(u"I select in the first select the entry with index 3")
def step_impl(context):
    select("#firstSelect", index="3")


@step(u"I select in the multiline select the entries with indexes 1, 3 and 5")
def step_impl(context):
    select("#multilineSelect", index=[1, "3", 5.0])


@step(u'I select in the multiline select the entries with indexes 4')
def step_impl(context):
    select("#multilineSelect", index=4)


@step(u"the value in the first select is '(.*?)'")
def step_impl(context, expected_value):
    assert_equals(expected_value, get_value("#firstSelect"))


@step(u"the values in the multiline select are 'b1value' and 'b4value'")
def step_impl(context):
    assert_equals(["b1value", "b4value"], get_value("#multilineSelect"))


@step(u"the values in the multiline select are 'b2value', 'b4value' and 'b6value'")
def step_impl(context):
    assert_equals(["b2value", "b4value", "b6value"], get_value("#multilineSelect"))


@step(u"the values in the multiline select are 'b1value', 'b3value' and 'b5value'")
def step_impl(context):
    assert_equals(["b1value", "b3value", "b5value"], get_value("#multilineSelect"))


@step(u"I deselect in the multiline select the entries with indexes 3 and 5")
def step_impl(context):
    deselect("#multilineSelect", index=[3, "5"])
