class Loop:
    def __init__(self,
                 loop_expression: str,
                 parallel: bool) -> None:
        self.loop_expression = loop_expression
        self.parallel = parallel
