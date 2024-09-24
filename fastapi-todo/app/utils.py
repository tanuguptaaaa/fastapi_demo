# utils.py
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

# Set up the CryptContext for hashing passwords using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

current_date = datetime.utcnow()


# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Generate a secret key
jwt_secret_key = "248623f0d47554a3f487006a1697f36b76bcad33afad417afa42ceb3f69902ff"
ALGORITHM = "HS256"


def generate_access_token(id: str) -> str:
    payload = {
        "sub": id,
        "exp": current_date + timedelta(minutes=15),  # Short-lived access token
        "iat": current_date,  # Issued at time
    }
    access_token = jwt.encode(payload, jwt_secret_key, algorithm=ALGORITHM)
    return access_token


def generate_refresh_token(id: str) -> str:
    payload = {
        "sub": id,
        "exp": current_date + timedelta(days=7),  # Long-lived refresh token
        "iat": current_date,
    }
    refresh_token = jwt.encode(payload, jwt_secret_key, algorithm=ALGORITHM)
    return refresh_token
