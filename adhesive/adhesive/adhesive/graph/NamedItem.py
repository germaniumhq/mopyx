from adhesive.graph.Item import Item


class NamedItem(Item):
    """
    An item in the process that has a name defined by the
    user.
    """
    def __init__(self,
                 *args,
                 id: str,
                 name: str) -> None:
        if args:
            raise Exception("You need to pass named arguments")

        super(NamedItem, self).__init__(id=id)

        if name is None:
            raise Exception(f"A named item ({self}) was created without a name.")

        self.name = name
