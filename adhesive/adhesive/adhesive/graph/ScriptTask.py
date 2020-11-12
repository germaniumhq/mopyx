from adhesive.graph.Process import Process
from adhesive.graph.ProcessTask import ProcessTask


class ScriptTask(ProcessTask):
    def __init__(self,
                 *args,
                 parent_process: Process,
                 id: str,
                 name: str,
                 language: str,
                 script: str) -> None:
        if args:
            raise Exception("You need to use named parameters")

        super(ScriptTask, self).__init__(
            parent_process=parent_process,
            id=id,
            name=name)

        self.language = language
        self.script = script
