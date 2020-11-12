from typing import Optional

from adhesive.graph.Item import Item


class Edge(Item):
    """
    An edge between two tasks in a Process.
    """
    def __init__(self,
                 *args,
                 id: str,
                 source_id: str,
                 target_id: str,
                 condition: Optional[str] = None) -> None:
        if args:
            raise Exception("You need to pass named arguments")

        super(Edge, self).__init__(id=id)

        self.source_id = source_id
        self.target_id = target_id
        self.condition = condition if condition else ''
