import adhesive
import unittest


test = unittest.TestCase()


@adhesive.task('Simple Looped Task')
def test_loop(context):
    test.assertEqual("simple", context.loop.expression)


@adhesive.task('Simple Nested Loop Task')
def test_nested_task(context):
    test.assertEqual("nested", context.loop.expression)
    test.assertEqual("parents", context.loop.parent_loop.expression)


@adhesive.task('Simple Nested Task')
def simple_nested_task(context) -> None:
    test.assertEqual("parents", context.loop.expression)


adhesive.process_start()\
    .task('Simple Looped Task', loop='simple')\
    .subprocess_start(loop="parents")\
        .task("Simple Nested Loop Task", loop="nested")\
        .task("Simple Nested Task")\
    .subprocess_end()\
    .build(initial_data={
        "simple": [1, 2, 3],
        "nested": [1, 2, 3],
        "parents": [1, 2, 3],
    })

