import bcrypt
import jwt
from datetime import datetime, timedelta
import os

# Define constant
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")  # Convert bytes to string for storage


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    data: dict, expires_delta: timedelta = timedelta(minutes=60)
) -> str:
    """Generate an access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, os.getenv("ACCESS_TOEKN_SECRET_KEY"), algorithm=ALGORITHM
    )


def create_refresh_token(
    data: dict, expires_delta: timedelta = timedelta(days=90)
) -> str:
    """Generate a refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, os.getenv("ACCESS_TOEKN_SECRET_KEY"), algorithm=ALGORITHM
    )

def verify_access_token(token: str) -> dict:
    """Verify the access token."""
    try:
        payload = jwt.decode(token, os.getenv("ACCESS_TOEKN_SECRET_KEY"), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"message": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"message": "Invalid token"}
