import adhesive


@adhesive.task('list shells in default shell')
def list_shells(context):
    context.workspace.run(f"""
        ls /bin
        ps -p $$
    """)


@adhesive.task('run bash shell')
def run_bash_shell(context):
    context.workspace.run(
        """
            ps -p $$ | grep bash
        """,
        shell="/bin/bash"
    )

    output = context.workspace.run_output(
        """
            ps -p $$ | grep bash
        """,
        shell="/bin/bash"
    )

    assert output


@adhesive.task('run dash shell')
def run_dash_shell(context):
    context.workspace.run(
        """
            ps -p $$ | grep dash
        """,
        shell="/bin/dash"
    )

    output = context.workspace.run_output(
        """
            ps -p $$ | grep dash
        """,
        shell="/bin/dash"
    )

    assert output


adhesive.build()
