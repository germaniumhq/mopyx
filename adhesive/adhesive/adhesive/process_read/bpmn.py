import re
import textwrap
from typing import Tuple, Optional, TypeVar, cast, Union, IO, TextIO
from xml.etree import ElementTree

from adhesive.graph.time.CycleTimerBoundaryEvent import CycleTimerBoundaryEvent
from adhesive.graph.time.DateTimerBoundaryEvent import DateTimerBoundaryEvent
from adhesive.graph.time.DurationTimerBoundaryEvent import DurationTimerBoundaryEvent
from adhesive.graph.ErrorBoundaryEvent import ErrorBoundaryEvent
from adhesive.graph.ProcessTask import ProcessTask
from adhesive.graph.ComplexGateway import ComplexGateway
from adhesive.graph.Edge import Edge
from adhesive.graph.EndEvent import EndEvent
from adhesive.graph.ExclusiveGateway import ExclusiveGateway
from adhesive.graph.Loop import Loop
from adhesive.graph.MessageEvent import MessageEvent
from adhesive.graph.ParallelGateway import ParallelGateway
from adhesive.graph.ScriptTask import ScriptTask
from adhesive.graph.StartEvent import StartEvent
from adhesive.graph.SubProcess import SubProcess
from adhesive.graph.Task import Task
from adhesive.graph.UserTask import UserTask
from adhesive.graph.Process import Process
from adhesive.graph.Lane import Lane

TAG_NAME = re.compile(r'^(\{.+\})?(.+)$')
SPACE = re.compile(r"\s+", re.IGNORECASE)

PT = TypeVar('PT', bound=ProcessTask)

ignored_elements = {
    # we obviously ignore extensions.
    "extensionElements",
    # we ignore the incoming and outgoing from inside the subprocesses
    # because we use the sequenceFlow elements to trace the connections.
    "incoming",
    "outgoing",
    # we ignore text annotations, and associations
    "textAnnotation",
    "association"
}

boundary_ignored_elements = set(ignored_elements)
boundary_ignored_elements.add("outputSet")


def read_bpmn_file(file_name: Union[str, IO[bytes], TextIO]) -> Process:
    """ Read a BPMN file as a build process. """
    root_node = ElementTree.parse(file_name).getroot()
    process = find_node(root_node, 'process')

    return read_process(None, process)


def find_node(parent_node, name: str):
    for node in list(parent_node):
        _, node_name = parse_tag(node)
        if node_name == name:
            return node

    return None


def get_boolean(parent_node, attr: str, default_value: bool) -> bool:
    attr_value = parent_node.get(attr)

    if attr_value is None:
        return default_value

    if attr_value.upper() == "TRUE":
        return True
    elif attr_value.upper() == "FALSE":
        return False

    raise Exception(f"Not a boolean value for {attr}: {attr_value}")


def read_process(parent_process: Optional[Process], process) -> Process:
    node_ns, node_name = parse_tag(process)

    if "process" == node_name:
        result = Process(
            id=process.get('id')
        )
    elif "subProcess" == node_name:
        assert parent_process
        result = SubProcess(
            parent_process=parent_process,
            id=process.get('id'),
            name=normalize_name(process.get('name'))
        )
    else:
        raise Exception(f"Unknown process node: {process.tag}")

    # we read first the nodes, then the boundary events,
    # then only the edges so they are findable
    # when adding the edges by id.
    for node in list(process):
        process_node(result, node)

    for node in list(process):
        process_boundary_event(result, node)

    for node in list(process):
        process_edge(result, node)

    for node in list(process):
        process_lane_set(result, node)

    for task_id, task in result.tasks.items():
        if not isinstance(task, ProcessTask):
            continue

        if result.has_incoming_edges(task):
            continue

        result.start_events[task.id] = task

    for task_id, task in result.tasks.items():
        if not result.has_outgoing_edges(task):
            if not isinstance(task, EndEvent) and not isinstance(task, ProcessTask):
                raise Exception(f"Executable node {task} has no outgoing connections, but can't "
                                f"be used as ae end task.")

            result.end_events[task.id] = task

    return result


def process_node(result: Process,
                 node) -> None:
    node_ns, node_name = parse_tag(node)

    if "task" == node_name:
        process_node_task(result, node)
    elif "userTask" == node_name:
        process_usertask(result, node)
    elif "scriptTask" == node_name:
        process_script_task(result, node)
    elif "sequenceFlow" == node_name:
        pass
    elif "boundaryEvent" == node_name:
        pass
    elif "standardLoopCharacteristics" == node_name:
        pass
    elif "startEvent" == node_name:
        process_node_start_event(result, node)
    elif "endEvent" == node_name:
        process_node_end_event(result, node)
    elif "subProcess" == node_name:
        process_node_sub_process(result, node)
    elif "exclusiveGateway" == node_name:
        process_exclusive_gateway(result, node)
    elif "parallelGateway" == node_name or "inclusiveGateway" == node_name:
        process_parallel_gateway(result, node)
    elif "complexGateway" == node_name:
        process_complex_gateway(result, node)
    elif "laneSet" == node_name:
        pass
    elif node_name not in ignored_elements:
        raise Exception(f"Unknown process node: {node.tag}")


def process_boundary_event(result: Process,
                           node) -> None:
    node_ns, node_name = parse_tag(node)

    if "boundaryEvent" == node_name:
        process_boundary_task(result, node)


def process_edge(result: Process,
                 node) -> None:
    node_ns, node_name = parse_tag(node)

    if "sequenceFlow" == node_name:
        process_node_sequence_flow(result, node)


def process_lane_set(process: Process,
                     result_set_node) -> None:
    """ Read the lane set and create lane objects for the lane """
    node_ns, node_name = parse_tag(result_set_node)

    if "laneSet" != node_name:
        return

    for node in list(result_set_node):
        node_ns, node_name = parse_tag(node)

        if node_name in boundary_ignored_elements:
            continue

        if node_name == "lane":
            process_lane(process, node)
            continue

        raise Exception(f"Unknown node <{node_name}> inside a <laneSet>.")


def process_lane(process: Process,
                 lane_node) -> None:
    """ Create a lane object """
    lane_node_ns, lane_node_name = parse_tag(lane_node)

    lane = Lane(id=lane_node.get("id"),
                name=lane_node.get("name"),
                parent_process=process)

    process.add_lane(lane)

    for node in list(lane_node):
        node_ns, node_name = parse_tag(node)

        if node_name in boundary_ignored_elements:
            continue

        if node_name == "flowNodeRef":
            process_lane_task(process, lane, node)
            continue

        raise Exception(f"Unknown node <{node_name}> inside a <{lane_node_name}>.")


def process_lane_task(
        process: Process,
        lane: Lane,
        xml_node
    ) -> None:
    """
    Binds the task for the lane.
    """
    task_id = textwrap.dedent(xml_node.text)
    process.add_task_to_lane(lane, task_id)


def process_node_task(p: Process, xml_node) -> None:
    """ Create a Task element from the process """
    node_name = normalize_name(xml_node.get("name"))
    task = Task(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name)

    task = process_potential_loop(task, xml_node)

    p.add_task(task)


def process_usertask(p: Process, xml_node) -> None:
    """ Create a HumanTask element from the process """
    node_name = normalize_name(xml_node.get("name"))
    task = UserTask(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name)

    task = process_potential_loop(task, xml_node)

    p.add_task(task)


def process_script_task(p: Process, xml_node) -> None:
    """ Create a ScriptTask element from the process """
    node_name = normalize_name(xml_node.get("name"))
    language = xml_node.get("scriptFormat")

    script_node = find_node(xml_node, "script")

    task = ScriptTask(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name,
        language=language,
        script=textwrap.dedent(script_node.text))

    task = process_potential_loop(task, xml_node)

    p.add_task(task)


def process_boundary_task(p: Process, boundary_event_node) -> None:
    """ Create a Task element from the process """
    for node in list(boundary_event_node):
        node_ns, node_name = parse_tag(node)

        if node_name in boundary_ignored_elements:
            continue

        # node is not ignored, we either found the type
        # or we die with exception.
        task_name = normalize_name(boundary_event_node.get("name"))

        if node_name == "errorEventDefinition":
            boundary_task = ErrorBoundaryEvent(
                parent_process=p,
                id=boundary_event_node.get("id"),
                name=task_name)

            boundary_task.attached_task_id = boundary_event_node.get(
                "attachedToRef", default="not attached")

            boundary_task.cancel_activity = get_boolean(
                boundary_event_node, "cancelActivity", True)
            boundary_task.parallel_multiple = get_boolean(
                boundary_event_node, "parallelMultiple", True)

            p.add_boundary_event(boundary_task)

            return

        if node_name == "timerEventDefinition":
            read_timer_event_definition(process=p,
                                        boundary_event_node=boundary_event_node,
                                        timer_event_definition_node=node,
                                        task_name=task_name)
            return


    raise Exception("Unable to find the type of the boundary event. Only "
                    "<errorEventDefinition>, and <timerEventDefinition> are supported.")


def read_timer_event_definition(*,
            process,
            boundary_event_node,
            timer_event_definition_node,
            task_name):

    for node in list(timer_event_definition_node):
        node_ns, node_name = parse_tag(node)

        if "timeCycle" == node_name:
            boundary_task = CycleTimerBoundaryEvent(
                parent_process=process,
                id=boundary_event_node.get("id"),
                name=task_name,
                expression=textwrap.dedent(node.text))
        elif "timeDuration" == node_name:
            boundary_task = DurationTimerBoundaryEvent(
                parent_process=process,
                id=boundary_event_node.get("id"),
                name=task_name,
                expression=textwrap.dedent(node.text))
        elif "timeDate" == node_name:
            boundary_task = DateTimerBoundaryEvent(
                parent_process=process,
                id=boundary_event_node.get("id"),
                name=task_name,
                expression=textwrap.dedent(node.text))
        elif node_name not in ignored_elements:
            raise Exception(f"Invalid node <{node_name}>, only <timeCycle>, <timeDuration> "
                            f"and <timeDate> are supported in a <timerEventDefinition>.")

    boundary_task.attached_task_id = boundary_event_node.get(
        "attachedToRef", default="not attached")

    boundary_task.cancel_activity = get_boolean(
        boundary_event_node, "cancelActivity", True)
    boundary_task.parallel_multiple = get_boolean(
        boundary_event_node, "parallelMultiple", True)

    process.add_boundary_event(boundary_task)


def process_node_start_event(p: Process, xml_node) -> None:
    """ Create a start event from the process """
    node_name = normalize_name(xml_node.get("name"))

    message_event_node = find_node(xml_node, "messageEventDefinition")

    if message_event_node is not None:
        message_event = MessageEvent(
            parent_process=p,
            id=xml_node.get("id"),
            name=node_name)

        p.add_message_event(message_event)
        return

    task = StartEvent(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name)

    p.add_start_event(task)


def process_node_end_event(p: Process, xml_node) -> None:
    """ Create an end event from the process """
    node_name = normalize_name(xml_node.get("name"))

    task = EndEvent(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name)

    p.add_end_event(task)


def process_node_sub_process(p: Process, xml_node) -> None:
    task = cast(SubProcess, read_process(p, xml_node))
    task = process_potential_loop(task, xml_node)

    p.add_task(task)


def process_node_sequence_flow(p: Process, xml_node) -> None:
    edge = Edge(id=xml_node.get("id"),
                source_id=xml_node.get("sourceRef"),
                target_id=xml_node.get("targetRef"))

    condition_node = find_node(xml_node, "conditionExpression")

    if condition_node is not None:
        edge.condition = textwrap.dedent(condition_node.text)

    p.add_edge(edge)


def process_exclusive_gateway(p: Process, xml_node) -> None:
    """ Create an exclusive gateway from the process """
    node_name = normalize_name(xml_node.get("name"))
    task = ExclusiveGateway(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name)

    p.add_task(task)


def process_parallel_gateway(p: Process, xml_node) -> None:
    """ Create an end event from the process """
    node_name = normalize_name(xml_node.get("name"))
    task = ParallelGateway(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name)

    p.add_task(task)


def process_complex_gateway(p: Process, xml_node) -> None:
    """ Create an end event from the process """
    node_name = normalize_name(xml_node.get("name"))

    task = ComplexGateway(
        parent_process=p,
        id=xml_node.get("id"),
        name=node_name)

    p.add_task(task)


def process_potential_loop(task: PT, xml_node) -> PT:
    loop_node = find_node(xml_node, "standardLoopCharacteristics")
    multi_instance_loop = find_node(xml_node, "multiInstanceLoopCharacteristics")

    if not loop_node and not multi_instance_loop:
        return task

    if loop_node and multi_instance_loop:
        raise Exception(f"Both standard loop and multi instance loop were present on {xml_node}")

    if loop_node:
        loop_expression = find_node(loop_node, "loopCondition")
        task.loop = Loop(loop_expression=textwrap.dedent(loop_expression.text),
                         parallel=True)
    elif multi_instance_loop:
        is_sequential = get_boolean(multi_instance_loop, "isSequential", False)
        loop_expression = find_node(multi_instance_loop, "completionCondition")
        task.loop = Loop(loop_expression=textwrap.dedent(loop_expression.text),
                         parallel=not is_sequential)
    else:
        raise Exception(f"No loop node was present, after the validation.")

    return task


def normalize_name(name: str) -> str:
    if not name:
        return "<noname>"

    return SPACE.sub(' ', name)


def parse_tag(node) -> Tuple[str, str]:
    m = TAG_NAME.match(node.tag)

    if not m:
        raise Exception(f"Unable to parse tag name `{node}`")

    return m[1], m[2]
