from typing import List, Any, Dict, Callable, Optional

class Compiler(object):
    def compile(
        self,
        source: Optional[str] = None,
        filename: Optional[str] = None,
        mode: Optional[str] = None,
        flags: List[str] = None,
        dont_inherit: bool = False,
        optimize: bool = False,
    ) -> Callable[[Dict[Any, Any]], str]:
        pass
