import sys

import oaas
import oaas_grpc

from features.steps.testsvc import testsvc_pb2
from features.steps.testsvc import testsvc_pb2_grpc

port = int(sys.argv[1])
process_name = sys.argv[3]


@oaas.service(sys.argv[2])
class ServiceName(testsvc_pb2_grpc.ProcessNameServicer):
    def get_process_name(self, request: testsvc_pb2.ProcessNameIn, context):
        return testsvc_pb2.ProcessNameOut(name=process_name)


# arg1 - port
# arg2 - service name
# arg3 - process name
def main():
    oaas.register_client_provider(oaas_grpc.OaasGrpcClient())
    oaas.register_server_provider(oaas_grpc.OaasGrpcServer(port=port))

    oaas.serve()
    print(f"test server running on {port}")
    oaas.join()


if __name__ == "__main__":
    main()
