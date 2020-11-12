import adhesive
import os
import unittest

test = unittest.TestCase()


@adhesive.lane('chdir')
def chdir_lane(context):
    context.workspace.pwd = os.curdir
    yield context.workspace


@adhesive.task('Try out the lane', lane="chdir")
def try_out_the_lane(context):
    test.assertEqual(os.curdir, context.workspace.pwd)


adhesive.build()
