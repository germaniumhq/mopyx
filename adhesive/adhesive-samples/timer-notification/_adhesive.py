import adhesive
import time


@adhesive.task('Potentially Long Running Task')
def potentially_long_running_task(context):
    time.sleep(3)


@adhesive.task('Notify Long Running Execution')
def notify_long_running_execution(context):
    pass


adhesive.bpmn_build(
    "timer-notification.bpmn",
    wait_tasks=False)
