from src.database import SessionLocal
from src.models import Role, User, Book


def seed_database():
    session = SessionLocal()
    try:
        if session.query(Role).first():
            print("[INFO] База данных уже содержит данные. Пропуск сидинга.")
            return

        print("[SEED] Создание начальных ролей...")
        admin_role = Role(name="admin")
        user_role = Role(name="user")
        session.add_all([admin_role, user_role])
        session.commit()

        print("[SEED] Создание тестовых пользователей...")
        admin = User(
            username="admin",
            email="admin@bookhub.local",
            password_hash="pbkdf2:admin_hash",
            role_id=admin_role.role_id
        )
        user = User(
            username="vika_reader",
            email="vika@mail.ru",
            password_hash="pbkdf2:user_hash",
            role_id=user_role.role_id
        )
        session.add_all([admin, user])
        session.commit()

        print("[SEED] Добавление начальных книг...")
        book1 = Book(
            title="1984",
            author="Джордж Оруэлл",
            genre="Антиутопия",
            annotation="Роман о тоталитарном обществе.",
            created_by=admin.user_id
        )
        book2 = Book(
            title="Преступление и наказание",
            author="Ф.М. Достоевский",
            genre="Классика",
            annotation="Психологический роман о границах дозволенного.",
            created_by=admin.user_id
        )
        session.add_all([book1, book2])
        session.commit()
        print("[SUCCESS] База данных успешно наполнена тестовыми данными!")

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()