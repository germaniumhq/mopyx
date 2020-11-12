import adhesive
import uuid
import addict
import unittest

test = unittest.TestCase()


@adhesive.task('Checkout Code')
def checkout_code(context):
    pass


@adhesive.task('GBS Test {loop.value.name}')
def gbs_test_loop_value_name_(context):
    pass


@adhesive.task('Ensure tool: version-manager')
def ensure_tool_version_manager(context):
    pass


@adhesive.task('Ensure tool: mypy')
def ensure_tool_mypy(context):
    pass


@adhesive.task('Ensure tool: flake8')
def ensure_tool_flake8(context):
    pass


@adhesive.task('Run tool: version-manager')
def run_tool_version_manager(context):
    pass


@adhesive.task('Run flake8')
def run_flake8(context):
    pass


@adhesive.task('Run mypy')
def run_mypy(context):
    pass


@adhesive.task('Prepare build')
def prepare_build(context):
    pass


@adhesive.task('GBS Build {loop.value.name}')
def gbs_build_loop_value_name_(context):
    context.data.past_builds = { str(uuid.uuid4()) }


data = adhesive.bpmn_build("build_python.bpmn", initial_data=addict.Dict({
	"build": {
		"run_mypy": True,
		"run_flake8": True,
		"binaries": [{"name":"x"}]
	}
}))

test.assertEqual(1,
				 len(data.past_builds),
				 "The builds were executed too many times")

