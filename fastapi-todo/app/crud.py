from sqlalchemy import or_
from sqlalchemy.orm import Session
from app import schemas
from app.models import ToDo, User
from app.schemas import ToDoCreate, ToDoUpdate
from app.utils import hash_password


def create_todo(db: Session, todo: ToDoCreate):
    db_todo = ToDo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session):
    return db.query(ToDo).all()


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(ToDo).filter(ToDo.id == todo_id).first()


def update_todo(db: Session, todo_id: int, todo_update: ToDoUpdate):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if db_todo:
        for key, value in todo_update.dict(exclude_unset=True).items():
            setattr(db_todo, key, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo


# crud.py
def create_user(db: Session, user: schemas.UserCreate):
    # Hash the user's password
    hashed_password = hash_password(user.password)

    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email_or_username(db: Session, email: str, username: str):
    query = db.query(User)
    if username and email:
        query = query.filter(or_(User.username == username, User.email == email))

    users = query.first()
    print("single-->", users)
    return users


def get_user_by_email(db: Session, email: str):
    query = db.query(User)
    if email:
        query = query.filter(User.email == email)

    users = query.first()
    print("single-->", users)
    return users


def update_user(db: Session, email: str, user_update: schemas.UserLogin):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        db_user.email = user_update.email
        db_user.hashed_password = hash_password(user_update.password)
        db.commit()
        db.refresh(db_user)
        return db_user