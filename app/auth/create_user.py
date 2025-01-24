from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session
import bcrypt

router = APIRouter()

class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserCreateResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

@router.post("/users", response_model=UserCreateResponse, summary="Create a new user", description="Endpoint to create a new user by providing username, password, and email.")
def create_user(user_request: UserCreateRequest, db: Session = Depends(get_sql_session)) -> UserCreateResponse:
    # Validate user input
    if db.query(User).filter(User.username == user_request.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == user_request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), bcrypt.gensalt())

    # Store the user in the database
    new_user = User(
        username=user_request.username,
        password_hash=hashed_password.decode('utf-8'),
        email=user_request.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserCreateResponse(id=new_user.id.__int__(), username=new_user.username.__str__(), email=new_user.email.__str__())
