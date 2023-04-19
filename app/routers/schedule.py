from typing import Optional, List, Union
from fastapi import Depends, APIRouter 
from pydantic import BaseModel
from database import Lesson, get_db
from sqlalchemy.orm import Session, joinedload
from database import *
import oauth2

router = APIRouter(
    tags=["Lesson"]
)

class SubjectResponseModel(BaseModel):
    id: int
    name: str
    color: str
    
    class Config:
        orm_mode = True

class LessonResponseModel(BaseModel):
    id: int
    class_id: int
    day: int
    subject_1_id: SubjectResponseModel
    subject_2_id: SubjectResponseModel
    subject_3_id: SubjectResponseModel
    subject_4_id: SubjectResponseModel
    subject_5_id: SubjectResponseModel
    subject_6_id: SubjectResponseModel
    teacher_id: str

    class Config:
        orm_mode = True


@router.get("/api/lessons", response_model=List[LessonResponseModel])
def get_lessons(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), day: Optional[int] = None):

    lessons = db.query(Lesson).filter(Lesson.class_id == current_user.class_id)
    if day:
        lessons = lessons.filter(Lesson.day == day)
    lessons = lessons.all()


    return lessons 