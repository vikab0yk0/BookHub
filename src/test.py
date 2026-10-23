from src.database import SessionLocal
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.repositories.review_repository import ReviewRepository
from src.repositories.user_book_repository import UserBookRepository


def run_demo():
    session = SessionLocal()
    try:
        print("\n" + "=" * 50)
        print(" СЦЕНАРИЙ 1: CRUD ОПЕРАЦИИ НАД КНИГОЙ (ADMIN)")
        print("=" * 50)
        book_repo = BookRepository(session)
        user_repo = UserRepository(session)
        admin = user_repo.get_by_username("admin")

        # CREATE
        book = book_repo.create(
            title="Мастер и Маргарита",
            author="М.А. Булгаков",
            genre="Мистика",
            annotation="Черновик аннотации",
            created_by=admin.user_id
        )
        print(f"-> [CREATE] Создана книга: ID={book.book_id}, Название='{book.title}'")

        # READ
        fetched_book = book_repo.get_by_id(book.book_id)
        print(f"-> [READ] Прочитано из БД: '{fetched_book.title}', Автор: {fetched_book.author}")

        # UPDATE
        book_repo.update(book.book_id, annotation="Культовый роман о визите дьявола в Москву.")
        print(f"-> [UPDATE] Аннотация обновлена: '{book_repo.get_by_id(book.book_id).annotation}'")

        print("\n" + "=" * 50)
        print(" СЦЕНАРИЙ 2: ЛИЧНЫЕ СПИСКИ И ОТЗЫВЫ (USER)")
        print("=" * 50)
        user = user_repo.get_by_username("vika_reader")
        ub_repo = UserBookRepository(session)

        ub_repo.add_to_list(user_id=user.user_id, book_id=book.book_id, status="favorite")
        print(f"-> [LIST] Книга добавлена в список 'favorite' пользователя {user.username}")

        rev_repo = ReviewRepository(session)
        review = rev_repo.create(
            user_id=user.user_id,
            book_id=book.book_id,
            rating=5,
            comment="Великолепное произведение, перечитываю третий раз!"
        )
        print(f"-> [REVIEW] Оставлен отзыв с оценкой {review.rating}/5")

        print("\n" + "=" * 50)
        print(" СЦЕНАРИЙ 3: ДЕМОНСТРАЦИЯ EAGER LOADING (БЕЗ N+1)")
        print("=" * 50)
        book_with_reviews = book_repo.get_with_reviews(book.book_id)
        print(f"-> Книга: {book_with_reviews.title}")
        for r in book_with_reviews.reviews:
            print(f"   * Отзыв от '{r.user.username}': {r.rating}/5 — «{r.comment}»")
        

        print("\n" + "=" * 50)
        print(" СЦЕНАРИЙ 4: КАСКАДНОЕ УДАЛЕНИЕ (DELETE)")
        print("=" * 50)
        book_repo.delete(book.book_id)
        print(f"-> [DELETE] Книга ID={book.book_id} удалена.")

        orphaned_review = session.get(type(review), review.review_id)
        print(f"-> Проверка отзыва в БД: {'Не найден (удален каскадно)' if not orphaned_review else 'Остался'}")

    finally:
        session.close()


if __name__ == "__main__":
    run_demo()