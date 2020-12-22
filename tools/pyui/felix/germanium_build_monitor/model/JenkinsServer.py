from typing import List, Dict, Any
from mopyx import model
import jenkins

from .JenkinsMonitoredJob import JenkinsMonitoredJob


@model
class JenkinsServer:
    def __init__(
            self,
            name: str = "",
            url: str = "http://localhost:8080/",
            use_authentication: bool = False,
            user: str = "",
            password: str = ""):

        self.name = name
        self.url = url
        self.use_authentication = use_authentication
        self.user = user
        self.password = password

        self.monitored_jobs: List[JenkinsMonitoredJob] = []

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "use_authentication": self.use_authentication,
            "user": self.user,
            "password": self.password,
            "monitored_jobs": [job.as_dict() for job in self.monitored_jobs]
        }

    @staticmethod
    def from_dict(d) -> 'JenkinsServer':
        result = JenkinsServer(
            d['name'],
            d['url'],
            d['use_authentication'],
            d['user'],
            d['password']
        )

        result.monitored_jobs = [JenkinsMonitoredJob.from_dict(mj) for mj in d['monitored_jobs']]

        return result


def jenkins_server(server: JenkinsServer) -> jenkins.Jenkins:
    if server.use_authentication:
        return jenkins.Jenkins(server.url,
                               username=server.user,
                               password=server.password)
    return jenkins.Jenkins(server.url)

