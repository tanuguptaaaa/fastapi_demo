from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas


TODO_NOT_FOUND = "ToDo not found"

router = APIRouter()

@router.get("/")
def index():
    return {"message":"hello,welcome"}

@router.post("/todos/", response_model=schemas.ToDoResponse)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@router.get("/todos/", response_model=list[schemas.ToDoResponse])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@router.get("/todos/{todo_id}", response_model=schemas.ToDoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo_by_id(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


@router.put("/todos/{todo_id}", response_model=schemas.ToDoResponse)
def update_todo(todo_id: int, todo_update: schemas.ToDoUpdate, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, todo_id, todo_update)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.delete_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return {"message": "ToDo deleted"}
