import adhesive
import unittest


test = unittest.TestCase()


@adhesive.task('Loop item')
def loop_item(context):
    context.data.execution_count += 1

    print(context.data.collection)

    if isinstance(context.data.collection, list):
        context.data.collection.pop()
    else:
        context.data.collection = ["a", "b", "c"]


data = adhesive.process_start()\
    .task("Loop item", loop="collection")\
    .process_end()\
    .build(initial_data={
        "execution_count": 0,
        "collection": True
    })


test.assertEqual(4, data.execution_count, "It should have executed four times")

