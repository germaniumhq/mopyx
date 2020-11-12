import oaas
import oaas_grpc
import sys
import signal

from features.steps.testsvc import testsvc_pb2_grpc
from features.steps.testsvc import testsvc_pb2


port = int(sys.argv[1])
service_name = sys.argv[2]
process_name = sys.argv[3]
tag_value = sys.argv[4]

instance_id = None


class ServiceName(testsvc_pb2_grpc.ProcessNameServicer):
    def get_process_name(self, request: testsvc_pb2.ProcessNameIn, context):
        return testsvc_pb2.ProcessNameOut(name=process_name)


def register_dynamic_service():
    global instance_id
    instance_id = oaas.publish(
        instance=ServiceName(),
        name=service_name,
        tags={"sometag": tag_value},
    )
    assert instance_id


def unregister_dynamic_service(a, b):
    assert instance_id
    oaas.unpublish(id=instance_id)
    print("service unregistered")


# arg1 - port
# arg2 - service name
# arg3 - process name
# arg4 - sometag value
def main():
    oaas.register_client_provider(oaas_grpc.OaasGrpcClient())
    oaas.register_server_provider(oaas_grpc.OaasGrpcServer(port=port))

    oaas.serve()

    register_dynamic_service()
    signal.signal(signal.SIGUSR2, unregister_dynamic_service)

    print(f"test server running on {port}")

    oaas.join()


print("loaded")


if __name__ == "__main__":
    main()
