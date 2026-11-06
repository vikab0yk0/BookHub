from collections import Counter
from sqlalchemy import select, func
from src.database import SessionLocal
from src.models.book import Book
from src.models.review import Review
from src.models.user_book import UserBook
from src.proto import recommendation_pb2, recommendation_pb2_grpc


class RecommendationServicer(recommendation_pb2_grpc.RecommendationServiceServicer):
    def GetRecommendations(self, request, context):
        user_id = request.user_id
        limit = request.limit if request.limit > 0 else 5

        print(f"\n[gRPC SERVER] >>> Получен запрос GetRecommendations: user_id={user_id}, limit={limit}")

        session = SessionLocal()
        try:
            read_or_listed = session.scalars(
                select(UserBook.book_id).where(UserBook.user_id == user_id)
            ).all()
            reviewed = session.scalars(
                select(Review.book_id).where(Review.user_id == user_id)
            ).all()
            excluded_book_ids = set(read_or_listed) | set(reviewed)


            favorite_books_ids = session.scalars(
                select(UserBook.book_id).where(
                    UserBook.user_id == user_id, 
                    UserBook.status.in_(["favorite", "read"])
                )
            ).all()

            high_rated_books_ids = session.scalars(
                select(Review.book_id).where(
                    Review.user_id == user_id, 
                    Review.rating >= 4
                )
            ).all()

            liked_book_ids = set(favorite_books_ids) | set(high_rated_books_ids)

            liked_genres = []
            if liked_book_ids:
                liked_genres = session.scalars(
                    select(Book.genre).where(Book.book_id.in_(liked_book_ids), Book.genre.isnot(None))
                ).all()

            genre_counts = Counter(liked_genres)
            top_genre = genre_counts.most_common(1)[0][0] if genre_counts else None

            print(f"[gRPC SERVER] Предпочтения пользователя user_id={user_id}: топ-жанр='{top_genre}', исключено книг={len(excluded_book_ids)}")


            candidates = session.scalars(
                select(Book).where(~Book.book_id.in_(excluded_book_ids) if excluded_book_ids else True)
            ).all()

            scored_recommendations = []
            for book in candidates:
                score = 3.0
                reason = "Рекомендация из каталога"


                if top_genre and book.genre == top_genre:
                    score += 2.0
                    reason = f"На основе вашего интереса к жанру «{top_genre}»"


                avg_rating = session.scalar(
                    select(func.avg(Review.rating)).where(Review.book_id == book.book_id)
                )
                if avg_rating:
                    score += float(avg_rating) * 0.5
                    if not top_genre or book.genre != top_genre:
                        reason = f"Высокий читательский рейтинг ({float(avg_rating):.1f}/5)"

                scored_recommendations.append((book.book_id, score, reason))


            scored_recommendations.sort(key=lambda x: x[1], reverse=True)
            selected = scored_recommendations[:limit]


            if not selected and candidates:
                selected = [(b.book_id, 1.0, "Популярная книга") for b in candidates[:limit]]

            response = recommendation_pb2.RecommendationResponse()
            for book_id, score, reason in selected:
                rec_item = response.recommendations.add()
                rec_item.book_id = book_id
                rec_item.score = round(score, 2)
                rec_item.reason = reason

            print(f"[gRPC SERVER] <<< Успешно сформировано {len(response.recommendations)} рекомендаций. Отправка ответа.")
            return response

        except Exception as e:
            print(f"[gRPC SERVER ERROR] Ошибка при расчете рекомендаций: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return recommendation_pb2.RecommendationResponse()
        finally:
            session.close()