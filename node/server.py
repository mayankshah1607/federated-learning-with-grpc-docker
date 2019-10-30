import grpc
from concurrent import futures
import time

import functions_pb2
import functions_pb2_grpc
import functions


class FederatedAppServicer(functions_pb2_grpc.FederatedAppServicer):

    def GenerateData(self, request, context):
        response = functions_pb2.Empty()
        response.value = functions.GenerateData()
        return response

    def SendModel(self, request, context):
        response = functions_pb2.Empty()
        response.value = functions.SendModel(request.model)
        return response

    def Train(self, request, context):
        response = functions_pb2.Model()
        response.model = functions.Train()
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

functions_pb2_grpc.add_FederatedAppServicer_to_server(FederatedAppServicer(), server)

print("Starting server on PORT: 8080")
server.add_insecure_port('[::]:8080')
server.start()

try:
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    server.stop(0)
