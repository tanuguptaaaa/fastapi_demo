from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.utils import verify_password

router = APIRouter()


# Basic users page for testing
@router.get("/users")
def user_index():
    return {"message": "Hello, welcome to the users app!"}


# Signup route
@router.post("/users/signup", response_model=schemas.UserResponse)
def signup_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email_or_username(db, user.email,user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email or Username already registered")
    return crud.create_user(db, user)


@router.put("/users/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")


    # a = verify_password(user.password, db_user.hashed_password)

    # Check if the password is correct
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful"}