import adhesive


@adhesive.task("Populate UI Data")
def task_impl(context) -> None:
    context.data.items = {
        "libcpprnt": ["wut"],
        "srv-core": ["wut"],
        "ucsj": ["wut"]
    }


@adhesive.usertask("Basic UI Task")
def task_ui_impl(context, ui) -> None:
    items = {
            "agent-windows": "a",
            "automation-engine-java": "b",
            "commons-java": "c",
            "initialdata": "d",
            "java-api": "e",
            "libcpprnt": "f",
            "msg-type": "g",
            "srv-core": "h",
            "syntax": "i",
            "uc-msl": "j",
            "ucsj": "k",
            "zusynchk": "l",
    }

    ui.add_checkbox_group("uicombo",
            value=context.data.items,
            values=items)


adhesive.build()
