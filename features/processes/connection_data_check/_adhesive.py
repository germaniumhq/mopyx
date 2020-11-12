import adhesive


@adhesive.task('Prepare data')
def prepare_data(context):
    context.data.data_is_set = True


@adhesive.task('Run if data is set via attribute name')
def run_if_data_is_set_via_attribute_name(context):
    context.data.set_via_attribute_name = True


@adhesive.task('Run if data is set via data.attribute')
def run_if_data_is_set_via_data_attribute(context):
    context.data.set_via_data_attribute = True


@adhesive.task('Run if data is set via context.data.attribute')
def run_if_data_is_set_via_context_data_attribute(context):
    context.data.set_via_context_data_attribute = True


data = adhesive.process_start()\
    .task("Prepare data")\
    .task("Run if data is set via attribute name", when="data_is_set")\
    .task("Run if data is set via data.attribute", when="data.data_is_set")\
    .task("Run if data is set via context.data.attribute", when="context.data.data_is_set")\
    .process_end()\
    .build()


assert data.set_via_attribute_name
assert data.set_via_data_attribute
assert data.set_via_context_data_attribute
