from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Any
import jwt
import os

from app.auth.authenticate_user import authenticate_user
from app.models.User import User

router = APIRouter()

# Define the secret key and algorithm for JWT
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/auth/login", response_model=TokenResponse, tags=["Authentication"])
def login(login_data: LoginRequest, user: User = Depends(authenticate_user)) -> Any:
    """
    Authenticate a user and return a JWT token.

    - **username**: The username of the user.
    - **password**: The password of the user.

    Returns a JWT token if authentication is successful.
    """
    # Create JWT token
    token_data = {"sub": user.username.__str__()}
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}
