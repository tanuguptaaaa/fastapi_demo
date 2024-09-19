from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255),index=True)
    description = Column(String(255))
    completed = Column(Boolean)
