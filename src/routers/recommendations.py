import grpc
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_session
from src.dependencies.grpc_client import get_recommendation_stub
from src.models.user import User
from src.proto import recommendation_pb2, recommendation_pb2_grpc
from src.repositories.book_repository import BookRepository
from src.schemas.book import BookShort
from src.schemas.recommendation import RecommendationItemOut, RecommendationListOut

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=RecommendationListOut, summary="Получить персональные рекомендации (через gRPC)")
def get_my_recommendations(
    limit: int = Query(5, ge=1, le=20, description="Количество рекомендаций"),
    current_user: User = Depends(get_current_user),
    stub: recommendation_pb2_grpc.RecommendationServiceStub = Depends(get_recommendation_stub),
    session: Session = Depends(get_session),
):
    """
    Запрашивает персональные рекомендации книг у внешнего gRPC-микросервиса.
    """
    print(f"\n[FastAPI] Получен HTTP-запрос /recommendations от user_id={current_user.user_id}")
    
    # 1. Формирование gRPC-запроса (Protobuf message)
    grpc_request = recommendation_pb2.RecommendationRequest(
        user_id=current_user.user_id,
        limit=limit,
    )

    # 2. Вызов удаленного метода через gRPC Stub с установкой дедлайна (3 секунды)
    try:
        print("[FastAPI] Отправка синхронного вызова GetRecommendations в gRPC-сервис...")
        grpc_response = stub.GetRecommendations(grpc_request, timeout=3.0)
    except grpc.RpcError as e:
        status_code = e.code()
        print(f"[FastAPI ERROR] Сбой вызова gRPC сервиса: {status_code} - {e.details()}")
        if status_code == grpc.StatusCode.UNAVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис рекомендаций временно недоступен",
            )
        elif status_code == grpc.StatusCode.DEADLINE_EXCEEDED:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Превышено время ожидания ответа от сервиса рекомендаций",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка сервиса рекомендаций: {e.details()}",
            )

    # 3. Обогащение результата данными о книгах из БД
    book_repo = BookRepository(session)
    result_items = []
    
    for rec in grpc_response.recommendations:
        book = book_repo.get_by_id(rec.book_id)
        if book:
            result_items.append(
                RecommendationItemOut(
                    book=BookShort.model_validate(book),
                    score=rec.score,
                    reason=rec.reason,
                )
            )

    print(f"[FastAPI] Ответ сформирован. Возвращено {len(result_items)} книг клиенту.\n")
    return RecommendationListOut(
        user_id=current_user.user_id,
        recommendations=result_items,
    )