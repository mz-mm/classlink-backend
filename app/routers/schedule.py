from typing import Optional, List, Union
from fastapi import Depends, APIRouter 
from pydantic import BaseModel
from database import Lesson, get_db
from sqlalchemy.orm import Session
from database import *
import oauth2

router = APIRouter(
    tags=["Lesson"]
)

class SubjectResponseModel(BaseModel):
    name: str
    
    class Config:
        orm_mode = True

class LessonResponseModel(BaseModel):
    id: int
    lesson_num : int
    subject: SubjectResponseModel
    day: str
    color: str

    class Config:
        orm_mode = True


@router.get("/api/lessons", response_model=List[LessonResponseModel])
def get_lessons(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), day: Optional[str] = None):

    user: Union[Student, Teacher, Parent, Admin] = db.query(Student).filter(Student.id == current_user.id).first()
    query = db.query(Lesson).join(Subject).filter(Lesson.class_id == user.class_id)
    if day:
        query = query.filter(Lesson.day == day)
    
    query = query.order_by(Lesson.day, Lesson.lesson_num)
    lessons = query.all()

    return lessons
