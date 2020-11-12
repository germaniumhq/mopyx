import textwrap
import unittest
from typing import cast

from adhesive.graph.ComplexGateway import ComplexGateway
from adhesive.graph.ErrorBoundaryEvent import ErrorBoundaryEvent
from adhesive.graph.ExclusiveGateway import ExclusiveGateway
from adhesive.graph.Loop import Loop
from adhesive.graph.ParallelGateway import ParallelGateway
from adhesive.graph.ProcessTask import ProcessTask
from adhesive.graph.ScriptTask import ScriptTask
from adhesive.graph.SubProcess import SubProcess
from adhesive.graph.Task import Task
from adhesive.graph.UserTask import UserTask
from adhesive.process_read.bpmn import read_bpmn_file


class TestReadingBpmn(unittest.TestCase):
    """
    Test if we can read a BPMN file correctly.
    """

    def test_reading_bpmn(self) -> None:
        """
        Try to see if reading a basic BPMN works.
        """
        process = read_bpmn_file("test/adhesive/xml/adhesive.bpmn")

        self.assertEqual(6, len(process.tasks))
        self.assertEqual(6, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        first_task = process.tasks["_3"]
        self.assertEqual("Build Germanium Image", first_task.name)

        self.assertTrue(process)

    def test_reading_subprocess_bpmn(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/adhesive_subprocess.bpmn")

        self.assertEqual(5, len(process.tasks))
        self.assertEqual(4, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        subprocess = cast(SubProcess, process.tasks["_7"])
        self.assertEqual("Test Browsers", subprocess.name)

        self.assertEqual(3, len(subprocess.tasks))
        self.assertEqual(1, len(subprocess.edges))
        self.assertEqual(2, len(subprocess.start_events))
        self.assertEqual(2, len(subprocess.end_events))

    def test_reading_exclusive_gateway_bpmn(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/exclusive_gateway.bpmn")

        self.assertEqual(6, len(process.tasks))
        self.assertEqual(6, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        task_route = process.edges["_9"]
        self.assertEqual('data.route == "task"', task_route.condition)

        task_route = process.edges["_10"]
        self.assertEqual('', task_route.condition)

    def test_reading_parallel_gateway_bpmn(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/gateway-parallel.bpmn")

        self.assertEqual(9, len(process.tasks))
        self.assertEqual(12, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        self.assertTrue(isinstance(process.tasks["_9"], ParallelGateway))

    def test_reading_gateway_exclusive_sign_bpmn(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/gateway-exclusive-sign.bpmn")

        self.assertEqual(7, len(process.tasks))
        self.assertEqual(8, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        self.assertTrue(isinstance(process.tasks["_3"], ExclusiveGateway))

    def test_reading_gateway_inclusive_sign_bpmn(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/gateway-inclusive.bpmn")

        self.assertEqual(8, len(process.tasks))
        self.assertEqual(10, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        self.assertTrue(isinstance(process.tasks["_3"], ParallelGateway))

    def test_reading_gateway_complex(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/gateway-complex.bpmn")

        self.assertEqual(8, len(process.tasks))
        self.assertEqual(10, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        self.assertTrue(isinstance(
            process.tasks["_4"],
            ComplexGateway
        ))

    def test_reading_error_event_interrupting(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/error-event-interrupting.bpmn")

        self.assertEqual(6, len(process.tasks))
        self.assertEqual(5, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        boundary_event: ErrorBoundaryEvent = cast(ErrorBoundaryEvent, process.tasks["_6"])
        self.assertTrue(isinstance(
            process.tasks["_6"],
            ErrorBoundaryEvent
        ))

        self.assertTrue(boundary_event.cancel_activity)
        self.assertFalse(boundary_event.parallel_multiple)

        parent_event: Task = cast(Task, process.tasks['_3'])
        self.assertEqual(parent_event.error_task, boundary_event)

    def test_reading_human_task(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/user-task.bpmn")

        self.assertEqual(3, len(process.tasks))
        self.assertEqual(2, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        self.assertTrue(isinstance(
            process.tasks["_3"],
            UserTask
        ))

    def test_reading_script_task(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/script.bpmn")

        self.assertEqual(4, len(process.tasks))
        self.assertEqual(3, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        self.assertTrue(isinstance(
            process.tasks["_3"],
            ScriptTask
        ))

        script_task: ScriptTask = cast(ScriptTask, process.tasks["_3"])
        self.assertEqual("text/python", script_task.language)
        self.assertEqual(textwrap.dedent("""\
            import uuid
            
            if not context.data.executions:
                context.data.executions = dict()
            
            if context.task.name not in context.data.executions:
                context.data.executions[context.task.name] = set()
            
            context.data.executions[context.task.name].add(str(uuid.uuid4()))"""), script_task.script)

    def test_reading_loop(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/loop.bpmn")

        self.assertEqual(5, len(process.tasks))
        self.assertEqual(5, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(1, len(process.end_events))

        self.assertTrue(isinstance(
            process.tasks["_5"],
            Task
        ))

        loop = cast(ProcessTask, process.tasks["_5"]).loop
        assert loop
        self.assertEqual("data.test_platforms", loop.loop_expression)

    def test_reading_message_event(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/message-event.bpmn")

        self.assertEqual(3, len(process.tasks))
        self.assertEqual(2, len(process.edges))
        self.assertEqual(0, len(process.start_events))
        self.assertEqual(1, len(process.message_events))
        self.assertEqual(1, len(process.end_events))

    def test_reading_event_timeouts(self) -> None:
        process = read_bpmn_file("test/adhesive/xml/event-timeout.bpmn")

        self.assertEqual(11, len(process.tasks))
        self.assertEqual(9, len(process.edges))
        self.assertEqual(1, len(process.start_events))
        self.assertEqual(0, len(process.message_events))
        self.assertEqual(2, len(process.end_events))

        evented_task = cast(ProcessTask, process.tasks["_3"])

        self.assertTrue(evented_task.timer_events)
        assert evented_task.timer_events
        self.assertEqual(5, len(evented_task.timer_events))

    def test_reading_unsupported_elements_fails(self) -> None:
        with self.assertRaises(Exception):
            read_bpmn_file("test/adhesive/xml/unsupported-call-activity.bpmn")


if __name__ == '__main__':
    unittest.main()
