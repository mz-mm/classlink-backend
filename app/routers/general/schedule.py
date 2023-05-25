from typing import Optional, List
from fastapi import Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import *
import oauth2


router = APIRouter(
    tags=["Lesson"]
)


class SubjectResponsModel(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        orm_mode = True


class LessonResponsModel(BaseModel):
    id: int
    class_id: int
    day: int
    lesson_num: int
    teacher_id: str
    subject: SubjectResponsModel

    class Config:
        orm_mode = True


@router.get("/api/schedule", response_model=List[LessonResponsModel])
def get_lessons(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), day: Optional[int] = None):
    lessons = db.query(Lesson).filter(Lesson.class_id == current_user.class_id).all()

    if day:
        lessons = lessons.filter(Lesson.day == day).all()

    return lessons
