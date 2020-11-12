class Item:
    """
    Any item inside a process, or the process itself that's identified by
    an id.
    """
    def __init__(self,
                 *args,
                 id: str):
        if args:
            raise Exception("You need to use named arguments.")

        if id is None:
            raise Exception(f"An item ({self}) was created without an id.")

        self.id = id
