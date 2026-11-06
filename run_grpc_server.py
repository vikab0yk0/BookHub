from concurrent import futures
import grpc
import sys

from src.proto import recommendation_pb2_grpc
from src.grpc_services.recommendation_servicer import RecommendationServicer


def serve(port: int = 50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendation_pb2_grpc.add_RecommendationServiceServicer_to_server(
        RecommendationServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"[gRPC SERVER] Сервер рекомендаций запущен на порту {port}")
    print(f"[gRPC SERVER] Ожидание входящих запросов по HTTP/2...")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\n[gRPC SERVER] Остановка сервера...")
        server.stop(0)


if __name__ == "__main__":
    serve()