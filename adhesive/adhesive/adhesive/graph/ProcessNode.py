from typing import Optional
import adhesive

from adhesive.graph.NamedItem import NamedItem


class ProcessNode(NamedItem):
    def __init__(self,
                 *args,
                 id: str,
                 name: str,
                 parent_process: Optional['adhesive.graph.Process.Process']) -> None:
        if args:
            raise Exception("You need to pass named arguments.")

        super(ProcessNode, self).__init__(id=id, name=name)

        #if not parent_process:
        #    raise Exception(f"A process node ({self}) was created without an actual parent process.")

        self.parent_process = parent_process

    @property
    def process_id(self) -> str:
        if not self.parent_process:
            return ""

        return self.parent_process.id
