from fastapi import APIRouter, Depends, status, HTTPException, responses
from sqlalchemy.orm import Session
from database import *
from utils import verify
import oauth2
from typing import Optional, Union


router = APIRouter(
    tags=["User"]
    )


@router.get("/api/user")
def get_user(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    user: Union[Student, Teacher, Parent, Admin] = db.query(Student).filter(Student.id == current_user.id).first()
    
    if not user:
        user = db.query(Teacher).filter(Teacher.id == current_user.id).first()
    
    if not user:
        user = db.query(Parent).filter(Parent.id == current_user.id).first()
     
    if not user:
        user = db.query(Admin).filter(Admin.id == current_user.id).first()
        
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    
    
    return user 