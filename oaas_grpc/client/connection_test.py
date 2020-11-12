import socket
import logging

LOG = logging.getLogger(__name__)


def is_someone_listening(location: str) -> bool:
    tokens = location.split(":")
    host_address = tokens[0]
    port = int(tokens[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a_socket:
        host_location = (host_address, port)
        try:
            LOG.debug("=> is_someone_listening(%s:%d)", host_address, port)
            result_of_check = a_socket.connect_ex(host_location)

            LOG.debug(
                "<= is_someone_listening(%s:%d) - %s",
                host_address,
                port,
                result_of_check == 0,
            )
            return result_of_check == 0
        except Exception as e:
            LOG.debug(f"<= is_someone_listening(%s:%d)", host_address, port, exc_info=e)
            return False
