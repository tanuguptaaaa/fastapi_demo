from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class ToDo(Base):
    """This table is for storing todo app"""
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255))
    completed = Column(Boolean, default= False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(512))
    reference_token = Column(String(512),index=True)
    otp = Column(String(6), nullable=True)

