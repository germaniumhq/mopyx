import unittest

from adhesive.execution.ExecutionToken import ExecutionToken
from adhesive.graph.ExecutableNode import ExecutableNode

from adhesive.model.ActiveEvent import ActiveEvent
from adhesive.model.ActiveEventStateMachine import ActiveEventState
from adhesive.model.ProcessEvents import ProcessEvents


class ProcessEventsTest(unittest.TestCase):
    def test_transitions(self):
        pe = ProcessEvents()

        context = ExecutionToken(
            task=ExecutableNode(id="_1", name="Test", parent_process=None),
            execution_id="root",
            token_id="root",
            data=None,
        )
        event = ActiveEvent(execution_id="root",
                            parent_id=None,
                            context=context)

        self.assertEqual({}, pe.events)

        pe[event.token_id] = event

        self.assertEqual(1, len(pe))
        self.assertEqual(1, len(pe.bystate[ActiveEventState.NEW]))
        self.assertEqual(0, len(pe.bystate[ActiveEventState.PROCESSING]))
        self.assertEqual(event, pe.get(ActiveEventState.NEW))
        self.assertIsNone(pe.get(ActiveEventState.PROCESSING))

        pe.transition(event=event, state=ActiveEventState.PROCESSING)

        self.assertEqual(1, len(pe))
        self.assertEqual(0, len(pe.bystate[ActiveEventState.NEW]))
        self.assertEqual(1, len(pe.bystate[ActiveEventState.PROCESSING]))
        self.assertIsNone(pe.get(ActiveEventState.NEW))
        self.assertEqual(event, pe.get(ActiveEventState.PROCESSING))
