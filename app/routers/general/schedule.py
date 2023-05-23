from typing import Optional, List, Union
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import *
import oauth2 as oauth2


router = APIRouter(
    tags=["Lesson"]
)


class LessonModel(BaseModel):
    id: int
    class_id: int
    day: int
    subjects: Optional[List[str]]

    class Config:
        orm_mode = True


@router.get("/api/schedule")
def get_lessons(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user), day: Optional[int] = None):
    query = db.query(Lesson).filter(Lesson.class_id == current_user.class_id)
    if day:
        query = query.filter(Lesson.day == day)
    lessons = query.order_by(
        Lesson.day,
        Lesson.subject_1_id,
        Lesson.subject_2_id,
        Lesson.subject_3_id,
        Lesson.subject_4_id,
        Lesson.subject_5_id,
        Lesson.subject_6_id
    ).all()
    lesson_models = []
    for lesson in lessons:
        subjects = [
            subject.name
            for subject in
            [lesson.subject_1, lesson.subject_2, lesson.subject_3, lesson.subject_4, lesson.subject_5, lesson.subject_6]
            if subject is not None
        ]
        lesson_model = LessonModel.from_orm(lesson)
        lesson_model.subjects = subjects
        lesson_models.append(lesson_model)

    return lesson_models
