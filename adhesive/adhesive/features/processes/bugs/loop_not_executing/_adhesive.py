from typing import List

import adhesive
import time
import logging
import sys

LOG = logging.getLogger(__name__)

PORT = 8000


class Data:
    namespace: str
    domain_names: List[str]
    test_mode: bool
    _error: Exception
    ingress_object: str


server_running = False


@adhesive.task('Run HTTP Server')
def start_http_server(context: adhesive.Token) -> None:
    global server_running

    while server_running:
        time.sleep(0.1)


@adhesive.task('Create service for registering the domain')
def create_service_for_registering_the_domain(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Delete service for registering domains')
def delete_service_for_registering_domains(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Wait for HTTP Server to be up')
def wait_for_http_server_to_be_up(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Wait for domain {loop.value}')
def wait_for_domain_loop_value_(context: adhesive.Token[Data]) -> None:
    assert context.loop
    pass


@adhesive.task('Patch Ingress Object {ingress_object}')
def patch_ingress_object_ingress_object_(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Revert Ingress Object {ingress_object}')
def revert_ingress_object_ingress_object_(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Add TLS secret to ingress {ingress_object}')
def add_tls_secret_to_ingress(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Create Certificate for {domain_name}')
def create_certificate_for_domain_name_(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Shutdown HTTP Server')
def stop_http_server(context: adhesive.Token) -> None:
    global server_running
    server_running = False


@adhesive.task('Create Secret {ingress_object}')
def create_secret_ingress_object_(context: adhesive.Token) -> None:
        pass


@adhesive.task('Log Error')
def log_error(context: adhesive.Token[Data]) -> None:
    pass


@adhesive.task('Exit with error')
def exit_with_error(context: adhesive.Token) -> None:
    sys.exit(2)


def wait_for_url(url: str) -> None:
    pass


domain_names = "domain.com"
kubernetes_namespace = "test"
ingress_object_name = "test"

adhesive.bpmn_build(
    "new-certificate.bpmn",
    initial_data={
        "namespace": kubernetes_namespace,
        "domain_names": domain_names.split(" "),
        "ingress_object": ingress_object_name,
    })
