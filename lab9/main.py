from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import  Column, Integer, String, ForeignKey
from fastapi import FastAPI

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True,  index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

#Добавление данных:
# Напишите программу, которая добавляет в таблицу Users несколько записей с разными значениями полей username, email и password.
# Напишите программу, которая добавляет в таблицу Posts несколько записей, связанных с пользователями из таблицы Users.

# user1 = User(username = "Dasha", email = "dasha@mail.ru", password = "dasha")
# user2 = User(username = "Slava", email = "slava@mail.ru", password = "slava")
# user3 = User(username = "Olesya", email = "olesya@mail.ru", password = "olesya")
# db.add_all([user1, user2, user3])
# db.commit()
#
# post1 = Post(title = "it", content = "about it", user_id = 1)
# post2 = Post(title = "plants", content = "about plants", user_id = 1)
# post3 = Post(title = "building", content = "about building", user_id = 2)
# post4 = Post(title = "books", content = "about books", user_id = 3)
# db.add_all([post1, post2, post3, post4])
# db.commit()

# Извлечение данных:
# Напишите программу, которая извлекает все записи из таблицы Users.
# Напишите программу, которая извлекает все записи из таблицы Posts. Включая информацию о пользователях, которые их создали.
# Напишите программу, которая извлекает записи из таблицы Posts, созданные конкретным пользователем.

users = db.query(User).all()
print("\nUsers: ")
for u in users:
    print(f"id: {u.id}, username: {u.username}, email: {u.email}, password: {u.password}")

posts = db.query(Post).all()
print("\nPosts: ")
for p in posts:
    user = db.get(User, p.user_id)
    print(f"id: {p.id}, title: {p.title}, content: {p.content}, username: {user.username}, email: {user.email}")

postsFilter = db.query(Post).filter(Post.user_id == 1).all()
print("\nPosts by user1: ")
for p in postsFilter:
    print(f"id: {p.id}, title: {p.title}, content: {p.content}, user_id: {p.user_id}")

# Обновление данных:
# Напишите программу, которая обновляет поле email у одного из пользователей.
# Напишите программу, которая обновляет поле content у одного из постов.

# user_to_update = db.get(User, 1)
# user_to_update.email = "dashadasha@mail.ru"
# db.commit()

# post_to_update = db.get(Post, 1)
# post_to_update.content = "hello, world"
# db.commit()

# Удаление данных:
# Напишите программу, которая удаляет один из постов.
# Напишите программу, которая удаляет пользователя и все его посты.

# post_to_delete = db.get(Post, 1)
# db.delete(post_to_delete)
# db.commit()

# user_to_delete = db.get(User, 1)
# posts_to_delete = db.query(Post).filter(Post.user_id == 1).all()
# for p in posts_to_delete:
#     db.delete(p)
# db.delete(user_to_delete)
# db.commit()

app = FastAPI()


