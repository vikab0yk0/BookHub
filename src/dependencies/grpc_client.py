from typing import Generator
import grpc
from src.proto import recommendation_pb2_grpc

GRPC_SERVER_HOST = "localhost:50051"


def get_recommendation_stub() -> Generator[recommendation_pb2_grpc.RecommendationServiceStub, None, None]:
    """Фабрика gRPC-канала и клиентской заглушки (Dependency Injection)."""
    channel = grpc.insecure_channel(GRPC_SERVER_HOST)
    stub = recommendation_pb2_grpc.RecommendationServiceStub(channel)
    try:
        yield stub
    finally:
        channel.close()