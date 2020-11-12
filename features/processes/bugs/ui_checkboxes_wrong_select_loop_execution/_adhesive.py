import adhesive


@adhesive.task("Prepare Loop Data")
def prepare_loop_data(context) -> None:
    context.data.loop_data = list( map(str, range(20)))


@adhesive.task("Loop on data", loop="data.loop_data")
def loop_on_data(context) -> None:
    out = context.workspace.run(f"echo {context.loop.value}", capture_stdout=True)

    context.data.selected_items = dict()

    if int(out) % 5 == 0:
        context.data.selected_items[out.strip()] = out.strip()


@adhesive.usertask("Display checkboxes every 5th checkbox")
def display_checkboxes_ui(context, ui) -> None:
    ui.add_checkbox_group("group",
            value=context.data.selected_items,
            values=context.data.loop_data)


adhesive.build()
