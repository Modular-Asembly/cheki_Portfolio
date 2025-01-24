from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Any
import bcrypt
import jwt
import os

from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session

# Define the secret key and algorithm for JWT
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"

# Pydantic model for input
class UserLogin(BaseModel):
    username: str
    password: str

# Pydantic model for output
class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter()

@router.post("/auth/login", response_model=Token, tags=["Authentication"])
def authenticate_user(user_login: UserLogin, db: Session = Depends(get_sql_session)) -> Any:
    """
    Authenticate a user and return a JWT token.

    - **username**: The username of the user.
    - **password**: The password of the user.
    """
    # Retrieve user by username
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password hash
    if not bcrypt.checkpw(user_login.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    token_data = {"sub": user.username.__str__()}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}
