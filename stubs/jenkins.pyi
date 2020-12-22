from typing import Optional, Any


class Jenkins:
    def __init__(self,
                 url: str,
                 username: Optional[str] = None,
                 password: Optional[str] = None):
        pass

    def get_all_jobs(self):
        pass

    def get_job_info(self, name: str, depth: Optional[str] = None) -> Any:
        pass
