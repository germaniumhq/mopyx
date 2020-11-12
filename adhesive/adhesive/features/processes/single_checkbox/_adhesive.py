import adhesive


@adhesive.task("Populate data")
def populate_data(context):
    context.data.branches = ["some/long/branch/name/incoming"]


@adhesive.usertask("Single Checkbox UI")
def single_checkbox(context, ui) -> None:
    ui.add_checkbox_group(
        "checkbox",
        title="0123456789012",
        values=context.data.branches
    )
    ui.add_radio_group(
        "radio",
        title="0123456789012",
        values=context.data.branches
    )


@adhesive.usertask("Single Checkbox ui 2")
def single_checkbox(context, ui) -> None:
    ui.add_checkbox_group(
        "checkbox2",
        title="01234567890123",
        values=context.data.branches,
    )
    ui.add_radio_group(
        "radio2",
        title="01234567890123",
        values=context.data.branches,
    )


adhesive.build()
