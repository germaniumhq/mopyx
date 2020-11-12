import time

import oaas
import oaas_grpc
from features.steps.testsvc.stdreader import read_stderr
from features.steps.testsvc.testsvc_pb2_grpc import ProcessNameStub

from features.support.model import BaseContext
from features.support.process_execution import ProcessExecution

oaas.register_client_provider(oaas_grpc.OaasGrpcClient())

oaas.client("process-name")(ProcessNameStub)


def before_scenario(context: BaseContext, scenario) -> None:
    """
    Before each scenario we're going to setup the registry, then
    tear it down.
    """
    context.client = None
    context.processes = dict()
    process = ProcessExecution(command=["python", "-m", "oaas_registry"])
    context.processes["registry"] = process

    while not "listening on 8999" in read_stderr(process):
        time.sleep(0.1)


def after_scenario(context: BaseContext, scenario) -> None:
    for process_name, process_execution in context.processes.items():
        process_execution.kill()
