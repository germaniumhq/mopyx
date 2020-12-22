from typing import List, cast
from mopyx import model, render_call, action
import unittest


@model
class Build:
    def __init__(self):
        self.name = "1"


@model
class Branch:
    def __init__(self):
        self.builds: List[Build] = []


@model
class Job:
    def __init__(self):
        self.branches: List[Branch] = []


@model
class Server:
    def __init__(self):
        self.jobs: List[Job] = []


@model
class RootModel:
    def __init__(self):
        self.servers: List[Server] = []


root_model: RootModel = cast(RootModel, RootModel())


class TestNestedListsRender(unittest.TestCase):
    """
    Try to see if nested lists also propagate changes correctly
    """

    def test_nested_lists_render(self):
        """
        Check nested lists.
        """
        events = []

        @render_call
        def render_servers() -> None:
            for server in root_model.servers:
                @render_call
                def render_server() -> None:
                    events.append("server")
                    for job in server.jobs:
                        @render_call
                        def render_job() -> None:
                            events.append("job")
                            for branch in job.branches:
                                @render_call
                                def render_branch() -> None:
                                    events.append("branch")
                                    for build in branch.builds:
                                        @render_call
                                        def render_build() -> None:
                                            events.append(f"build {build.name}")

        self.assertEqual([], events)

        server = Server()
        server.jobs.append(Job())
        server.jobs[0].branches.append(Branch())
        server.jobs[0].branches[0].builds.append(Build())

        self.assertEqual([], events)

        root_model.servers.append(server)

        self.assertEqual(['server', 'job', 'branch', 'build 1'], events)
        events = []

        server.jobs[0].branches[0].builds[0].name = "2"
        self.assertEqual(['build 2'], events)

        events = []

        branch = Branch()
        branch.builds.append(Build())
        branch.builds.append(Build())

        @action
        def action_call():
            server.jobs[0].branches = [branch]

        action_call()
        self.assertEqual(['job', 'branch', 'build 1', 'build 1'], events)


if __name__ == '__main__':
    unittest.main()
