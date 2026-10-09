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
            title="Братья Карамазовы", 
            author="Ф.М. Достоевский", 
            genre="Классика", 
            annotation="Последний роман писателя, где убийство отца, суд и духовные метания Дмитрия, Ивана и Алёши становятся поводом для размышлений о вере, свободе, вине и искуплении.", 
            created_by=admin.user_id
        )
        book2 = Book(
            title="Пробуждение Левиафана", 
            author="Дж. Кори", 
            genre="Фантастика", 
            annotation="Первый том цикла «The Expanse»: нуарная охота за пропавшей девушкой на Церере и находка таинственной протомолекулы командой «Кентербери» сплетают судьбы детектива Миллера и капитана Холдена в заговор, который грозит столкнуть Землю, Марс и Пояс в войну за будущее Солнечной системы.", 
            created_by=admin.user_id
        )
        book3 = Book(
            title="Отчаяние", 
            author="В.В. Набоков", 
            genre="Роман", 
            annotation="Эмигрант принимает бродягу за своего двойника и задумывает идеальное убийство ради страховки – история самообмана и ненадёжного рассказчика.", 
            created_by=admin.user_id
        )
        book4 = Book(
            title="Тень над Инсмутом", 
            author="Г.В. Лавкрафт", 
            genre="Хоррор", 
            annotation="Путешественник попадает в полузаброшенный портовый городок и раскрывает жуткий сговор его вырождающихся жителей с древними морскими существами из глубин океана.", 
            created_by=admin.user_id
        )
        session.add_all([book1, book2, book3, book4])
        session.commit()
        print("[SUCCESS] База данных успешно наполнена тестовыми данными!")

    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
