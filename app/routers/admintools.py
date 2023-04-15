from typing import Optional, List, Union
from fastapi import Depends, APIRouter 
from pydantic import BaseModel
from database import Lesson, get_db
from sqlalchemy.orm import Session
from database import *
import oauth2

router = APIRouter(
    tags=["admin tools"]
)

class LessonPostModel(BaseModel):
    class_id: int
    subject_id: int
    day: int
    subject_1_id: int
    subject_2_id: int
    subject_3_id: int
    subject_4_id: int
    subject_5_id: int
    subject_6_id: int
    teacher_id: int

    class Config:
        orm_mode = True

@router.post("/api/admintools/schedule",)
def create_schedule(lesson: LessonPostModel, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    
    return new_lesson
