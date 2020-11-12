import adhesive


# Test labels picked from values
@adhesive.usertask("Pick The Left Button")
def pick_left_button(context, ui) -> None:
    ui.add_default_button("button", value="left")
    ui.add_default_button("button", value="right")


@adhesive.task("Validate Left Button Was Pressed")
def validate_left_button(context) -> None:
    assert context.data.button == "left"


# Test labels picked from labels
@adhesive.usertask("Pick The Right Button")
def pick_right_button(context, ui) -> None:
    ui.add_default_button("button",
                          title="Left",
                          value="left")
    ui.add_default_button("button",
                          title="Right",
                          value="right")


@adhesive.task("Validate Right Button Was Pressed")
def validate_right_button(context) -> None:
    assert context.data.button == "right"


# Test labels picked from names
@adhesive.usertask("Pick The Middle Button")
def pick_middle_button(context, ui) -> None:
    ui.add_default_button("left", value=True)
    ui.add_default_button("middle", value=True)
    ui.add_default_button("right", value=True)


@adhesive.task("Validate Middle Button Was Pressed")
def validate_middle_button(context) -> None:
    assert not context.data.left
    assert context.data.middle
    assert not context.data.right


adhesive.build()
