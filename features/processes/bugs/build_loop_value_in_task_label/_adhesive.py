import adhesive


@adhesive.task('create data')
def create_data(context):
    context.data.items = ["a", "b", "c"]


@adhesive.task("it's item {loop.value}", loop="items")
def iterate_item(context):
    print(context.loop.value)


adhesive.build()
