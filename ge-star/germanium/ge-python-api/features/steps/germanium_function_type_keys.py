from behave import *

from germanium.static import *


@step(u'there is no error message.')
def step_impl(context):
    assert Text('NO ERROR').exists()
