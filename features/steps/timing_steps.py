from behave import *
import time

use_step_matcher("re")


@step("I start timing the passed time")
def start_timing_the_passed_time(context):
    context.start_time = int(round(time.time() * 1000))


@step("the passed time is less than ten seconds")
def time_passed_is_less_than_two_seconds(context):
    end_time = int(round(time.time() * 1000))
    assert end_time - context.start_time < 10000
