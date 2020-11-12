import adhesive


@adhesive.task('Sleep 2 seconds')
def sleep_2_seconds(context: adhesive.Token) -> None:
    context.workspace.run("""
        sleep 2
    """)


@adhesive.task('Should not execute')
def should_not_execute(context: adhesive.Token) -> None:
    raise Exception("The timer should have cancelled the subprocess")


adhesive.bpmn_build("cancel-nested-subprocess.bpmn")
