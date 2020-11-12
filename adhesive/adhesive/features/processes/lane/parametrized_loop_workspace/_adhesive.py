import adhesive
import unittest

test = unittest.TestCase()


@adhesive.task('Hello {loop.value}')
def hello_loop_value_(context):
    pass


@adhesive.lane('server: {loop.value}')
def lane_server_loop_value_(context):
    context.data.lane_names = set()
    context.data.lane_names.add(context.lane.name)
    context.data.lane_count += 1

    yield context.workspace.clone()


data = adhesive.bpmn_build("parametrized-loop-workspace.bpmn",
	initial_data={
		"items": ["a", "b", "c"],
        "lane_count": 0,
	})

test.assertEqual(data.lane_names, {
	"server: {loop.value}",
}, "There should be a single lane for all the iterations")
test.assertEqual(1, data.lane_count, "There should be a single lane for all the iterations")
