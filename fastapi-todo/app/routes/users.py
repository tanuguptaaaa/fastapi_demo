from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.email_helper import send_email
from app.utils import verify_password, generate_access_token, generate_refresh_token, generate_otp, hash_password

router = APIRouter()


# Basic users page for testing
@router.get("/users")
def user_index():
    return {"message": "Hello, welcome to the users app!"}


# Signup route
@router.post("/users/signup", response_model=schemas.SignupResponse)
def signup_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email_or_username(db, user.email, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email  or username is already registered")
    return crud.create_user(db, user)


def generate_reference_token():
    return str(uuid4())


# Login route
@router.put("/users/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Check if the password is correct
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = generate_access_token(db_user.id)
    refresh_token = generate_refresh_token(db_user.id)
    if not db_user.reference_token:
        db_user.reference_token = generate_reference_token()
        db.commit()
        db.refresh(db_user)
    # Output tokens
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    return schemas.UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        access_token=access_token,
        refresh_token=refresh_token,
        reference_token=db_user.reference_token,
    )


# Assuming you have a utility function for sending emails
@router.post("/users/forgot-password")
async def forgot_password(user: schemas.UserForgot, db: Session = Depends(get_db)):
    # Check if the user with the provided email exists
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")

    otp = generate_otp()
    db_user.otp = otp
    db.commit()
    db.refresh(db_user)

    email_content = f"<h1>Your OTP for password reset is: {otp}</h1>"

    try:
        await send_email(user.email, email_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error sending email")

    return {"message": "OTP sent to your email"}


@router.post("/users/reset-password")
def reset_password(user: schemas.UserReset, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify OTP
    if db_user.otp != user.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Reset the password
    db_user.hashed_password = hash_password(user.new_password)  # Correctly hash the password
    db_user.otp = None  # Clear the OTP after password reset
    db.commit()
    db.refresh(db_user)

    return {"message": "Password reset successful"}



