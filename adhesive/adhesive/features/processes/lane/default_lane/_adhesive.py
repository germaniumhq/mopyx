import adhesive
import os
import unittest


test = unittest.TestCase()


@adhesive.lane('default')
def default_lane(context):
    context.workspace.pwd = os.curdir
    yield context.workspace


@adhesive.task('Check default lane')
def default_lane_check(context):
    test.assertEqual(os.curdir, context.workspace.pwd)


adhesive.build()
