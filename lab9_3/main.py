from sqlalchemy.orm import Session, DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse

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

# Реализация CRUD-операций:
# Реализуйте веб-страницы для выполнения CRUD-операций (создание, чтение, обновление, удаление) с записями в таблицах Users и Posts.
# Страницы должны включать:
# Форму для создания нового пользователя/поста.
# Список всех пользователей/постов с возможностью редактирования и удаления.
# Страницу для редактирования информации о пользователе/посте.

app = FastAPI()

@app.get("/users")
def main():
    return FileResponse("users.html")

@app.get("/posts")
def main():
    return FileResponse("posts.html")

@app.get("/api/users")
def get_users():
    return db.query(User).all()

@app.get("/api/users/{id}")
def get_user(id):
    user = db.get(User, id)
    if user==None:
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    return user

@app.post("/api/users")
def create_user(data=Body()):
    user = User(username=data["username"], email=data["email"], password =data["password"])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.put("/api/users")
def edit_user(data=Body()):
    user = db.get(User, data["id"])
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user.username = data["username"]
    user.email = data["email"]
    user.password = data["password"]
    db.commit()
    db.refresh(user)
    return user

@app.delete("/api/users/{id}")
def delete_user(id):
    user = db.get(User, id)
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    db.delete(user)
    db.commit()
    return user

@app.get("/api/posts")
def get_posts():
    return db.query(Post).all()

@app.get("/api/posts/{id}")
def get_post(id):
    post = db.get(Post, id)
    if post==None:
        return JSONResponse(status_code=404, content={ "message": "Пост не найден"})
    return post

@app.post("/api/posts")
def create_post(data=Body()):
    post = Post(title=data["title"], content=data["content"], user_id=data["user_id"])
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.put("/api/posts")
def edit_post(data=Body()):
    post = db.get(Post, data["id"])
    if post == None:
        return JSONResponse(status_code=404, content={"message": "Пост не найден"})
    post.title = data["title"]
    post.content = data["content"]
    post.user_id = data["user_id"]
    db.commit()
    db.refresh(post)
    return post

@app.delete("/api/posts/{id}")
def delete_post(id):
    post = db.get(Post, id)
    if post == None:
        return JSONResponse(status_code=404, content={"message": "Пост не найден"})
    db.delete(post)
    db.commit()
    return post