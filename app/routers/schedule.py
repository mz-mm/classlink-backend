from typing import Optional, List, Union
from fastapi import FastAPI, Response, HTTPException, status, Form, Depends, Body, APIRouter
from pydantic import BaseModel, EmailStr
from database import Lesson, get_db
from sqlalchemy.orm import Session
from datetime import datetime
from database import *
import oauth2

router = APIRouter(
    tags=["Lesson"]
)


@router.get("/api/lessons")
def get_lessons(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), day: Optional[str] = None):
    
    user: Union[Student, Teacher, Parent, Admin] = db.query(Student).filter(Student.id == current_user.id).first()
    
    
    if day:
        lessons = db.query(Lesson).filter(Lesson.class_id == user.class_id, Lesson.day == day).all()
    if not day:
        lessons = db.query(Lesson).filter(Lesson.class_id == user.class_id).all()
    
        
    return lessons 
