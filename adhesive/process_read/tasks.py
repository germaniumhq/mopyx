from adhesive import ExecutionTask, ExecutionUserTask

from adhesive.graph.Process import Process
from adhesive.model.AdhesiveProcess import AdhesiveProcess
from adhesive.process_read.programmatic import generate_from_calls


def generate_from_tasks(process: AdhesiveProcess) -> Process:
    if not process.chained_task_definitions:
        raise Exception("No task was defined. You need to create "
                        "tasks with @adhesive.task or @adhesive.usertask .")

    builder = generate_from_calls(None)

    for task in process.chained_task_definitions:
        if isinstance(task, ExecutionTask):
            builder.task(task.expressions[0],
                         when=task.when,
                         loop=task.loop,
                         lane=task.lane)
        elif isinstance(task, ExecutionUserTask):
            builder.usertask(task.expressions[0],
                              when=task.when,
                              loop=task.loop,
                              lane=task.lane)
        else:
            raise Exception(f"Unsupported task {task}")

    builder.process_end()

    return builder.process
