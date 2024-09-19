from pydantic import BaseModel


class ToDoCreate(BaseModel):
    title: str
    description: str


class ToDoUpdate(BaseModel):
    title: str
    description: str
    completed: bool


class ToDoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True  # Allow ORM objects to be returned as responses
