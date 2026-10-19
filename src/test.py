from src.database import SessionLocal
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.repositories.review_repository import ReviewRepository
from src.repositories.user_book_repository import UserBookRepository

from sqlalchemy import select, func, inspect
from src.models.review import Review
from src.models.book import Book
from src.models.bookmark import Bookmark

from src.models import Role, User

from statistics import mean

def run_test():
    session = SessionLocal()
    try:
        print("\n\n\nCRUD ОПЕРАЦИИ НАД КНИГОЙ")
        book_repo = BookRepository(session)
        user_repo = UserRepository(session)
        admin = user_repo.get_by_username("admin")
        
        # CREATE
        book = book_repo.create(
            title="Последнее желание",
            author="А. Сапковский",
            genre="Фэнтези",
            annotation="Черновик аннотации",
            created_by=admin.user_id
        )
        # print(f"-> [CREATE] Создана книга: ID={book.book_id}, Название='{book.title}'")
        print(f"\n\n--------------> [CREATE] Создана книга\n\n")

        user_book_repo = UserBookRepository(session)
        userbook = user_book_repo.add_to_list(admin.user_id, book.book_id, 'favorite')
        # print(inspect(userbook).transient)

        # # READ
        fetched_book = book_repo.get_by_id(book.book_id)
        print(f"-> [READ] Прочитано из БД: '{fetched_book.title}', Автор: {fetched_book.author}")
        print(f"\n\n--------------> [READ] Прочитано из БД\n\n")

        # # UPDATE
        book_repo.update(book.book_id, annotation="Открывающий цикл «Ведьмак» сборник рассказов о Геральте из Ривии – наёмном охотнике на чудовищ, который в мире, где монстры порой благороднее людей, пытается исполнить последнее желание и не потерять себя.")
        print(f"-> [UPDATE] Аннотация обновлена: '{book_repo.get_by_id(book.book_id).annotation}'")

        print("\n\n\nЛИЧНЫЕ СПИСКИ И ОТЗЫВЫ (USER)")
        user = user_repo.get_by_username("vika_reader")
        ub_repo = UserBookRepository(session)
        
        # Добавление в личный список (N:M)
        ub_repo.add_to_list(user_id=user.user_id, book_id=book.book_id, status="favorite")
        # print(f"-> [LIST] Книга добавлена в список 'favorite' пользователя {user.username}")
        print(f"\n\n--------------> [LIST] Книга добавлена в список\n\n")

        # Оставление отзыва
        rev_repo = ReviewRepository(session)
        review = rev_repo.create(
            user_id=user.user_id, 
            book_id=book.book_id, 
            rating=5, 
            comment="Великолепное произведение, перечитываю третий раз!"
        )
        # print(f"-> [REVIEW] Оставлен отзыв с оценкой {review.rating}/5")
        print(f"\n\n--------------> [REVIEW] Оставлен отзыв с оценкой\n\n")

        print("\n\n\nLOADING")
        book_with_reviews = book_repo.get_with_reviews(book.book_id)
        print(f"-> Книга: {book_with_reviews.title}")
        for r in book_with_reviews.reviews:
            print(f"   * Отзыв от '{r.user.username}': {r.rating}/5 — «{r.comment}»")

        print("\n\n\nDELETE")
        book_repo.delete(book.book_id)
        print(f"-> [DELETE] Книга ID={book.book_id} удалена.")
        
        # Удаление отзыва
        orphaned_review = session.get(type(review), review.review_id)
        print(f"-> Проверка отзыва в БД: {'Не найден (удален каскадно)' if not orphaned_review else 'Остался'}")


        # Книга с отзывом но без закладок
        
        # has_review = select(Review.review_id).where(Review.book_id == Book.book_id, Review.user_id == 2).exists()
        # has_bookmark = select(Bookmark.bookmark_id).where(Bookmark.book_id == Book.book_id, Bookmark.user_id == 2).exists()
        # books = session.scalars(select(Book).where(has_review, ~has_bookmark).order_by(Book.title)).all()

        stmt = (
            select(Book)
            .outerjoin(Review, (Review.book_id == Book.book_id) & (Review.user_id == 2))
            .outerjoin(Bookmark, (Bookmark.book_id == Book.book_id) & (Bookmark.user_id == 2))
            .group_by(Book.book_id)
            .having(
                func.count(Review.review_id) >0,
                func.count(Bookmark.bookmark_id) ==0
            )
        )
        books = session.scalars(stmt).all()

        print("\n\nКниги с отзывом, но без закладок:")
        if not books:
            print("\n\nНет таких книг")
        else:
            for b in books:
                print(b.title, " ", b.author)

        # автор, у которого самая высокая средняя оценка книг (не sql)
        data_books = session.scalars(select(Book)).all()
        data_reviews = session.scalars(select(Review)).all()

        author_by_book = {b.book_id: b.author for b in data_books}
        by_author = {}
        for r in data_reviews:
            author = author_by_book.get(r.book_id)
            if not author: continue
            if author not in by_author:
                by_author[author]=[]
            by_author[author].append(r.rating)
        top = sorted(by_author, key=lambda x: mean(by_author[x]))[-1]
        print(f"\n\n!!! ТОП 1 АВТОР - {top} !!!\n\n")

    finally:
        session.close()

if __name__ == "__main__":
    run_test()
