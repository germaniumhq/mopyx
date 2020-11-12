import time

import oaas
import oaas_transport_grpc

import adhesive

event_queue = []


@oaas.service("event-generator")
class EventGenerator:
    def generate_event(self) -> None:
        event_queue.append("x")


@oaas.client("event-registry")
class EventRegistry:
    def is_event_done(self, *, event_id: str, task_name: str) -> bool:
        ...

    def has_events(self) -> bool:
        ...


@adhesive.message('Generate events')
def message_rest_rest_process_resource(context):
    event_registry = oaas.get_client(EventRegistry)
    index = 0

    while event_registry.has_events():
        for _ in event_queue:
            yield {
                "id": "a",
                "index": index
            }
            index += 1

        time.sleep(0.1)


@adhesive.task('Deduplicate Task on {event.id}', deduplicate='event.id')
def deduplicate_task(context: adhesive.Token) -> None:
    event_registry = oaas.get_client(EventRegistry)

    while not event_registry.is_event_done(
            event_id=context.token_id,
            task_name=context.task_name):
        time.sleep(0.1)


@adhesive.task('Fail first execution')
def fail_first_execution(context: adhesive.Token) -> None:
    if context.data.event["index"] == 0:
        raise Exception("task failed")


oaas.register_client_provider(oaas_transport_grpc.OaasGrpcTransportClient())
oaas.register_server_provider(oaas_transport_grpc.OaasGrpcTransportServer())


oaas.serve()
adhesive.bpmn_build("deduplicate_fail_downstream.bpmn", wait_tasks=False)
