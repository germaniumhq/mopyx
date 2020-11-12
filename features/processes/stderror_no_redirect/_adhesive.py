import adhesive
from adhesive.config import current

current.stdout = True


@adhesive.task('Run a failing task')
def run_failing_task(context):
    context.workspace.run("""
        echo "test"
        false
    """)


adhesive.build()
