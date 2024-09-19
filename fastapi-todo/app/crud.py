from sqlalchemy.orm import Session

from app.models import ToDo
from app.schemas import ToDoCreate, ToDoUpdate


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
