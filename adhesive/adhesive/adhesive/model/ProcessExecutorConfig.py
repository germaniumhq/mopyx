class ProcessExecutorConfig:
    def __init__(self,
                 wait_tasks: bool = True) -> None:
        self.wait_tasks = wait_tasks
