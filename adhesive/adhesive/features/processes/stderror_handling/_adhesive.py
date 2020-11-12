import adhesive


@adhesive.task("Some task")
def throw_some_exception(context) -> None:
    raise Exception("Custom exception was thrown")


adhesive.build()