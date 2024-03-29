from fastapi import APIRouter, Depends, status, HTTPException, responses
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import *
from pydantic import BaseModel
from util import verify
import oauth2
from rate_limit import rate_limited, Request
from typing import Optional, Union

router = APIRouter(
    tags=["Authentication"]
)


class LoginModel(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


@router.post("/api/login", response_model=Token)
@rate_limited(max_calls=100, time_frame=60)
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: Union[Student, Teacher, Parent, Admin] = db.query(Student).filter(
        Student.email == user_credentials.username).first()
    role = "student"

    if not user:
        user = db.query(Teacher).filter(Teacher.email == user_credentials.username).first()
        role = "teacher"
    if not user:
        user = db.query(Parent).filter(Parent.email == user_credentials.username).first()
        role = "parent"
    if not user:
        user = db.query(Admin).filter(Admin.email == user_credentials.username).first()
        role = "admin"

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id, "name": user.full_name, "role": role})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/api/verifytoken")
def verify_token(current_user: str = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True}
