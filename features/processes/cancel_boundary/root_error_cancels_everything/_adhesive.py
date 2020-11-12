import adhesive
import sys


@adhesive.task('Raise Exception')
def raise_exception(context):
    raise Exception("ded")


@adhesive.task('Wait 2 seconds')
def wait_2_secs(context):
    context.workspace.run("""
        sleep 2
    """)


adhesive.process_start()\
    .branch_start()\
        .task('Raise Exception')\
    .branch_end()\
    .branch_start()\
        .task('Wait 2 seconds')\
    .branch_end()\
    .process_end()\
    .build()
