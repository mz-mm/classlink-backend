from typing import Optional, List, Union
from fastapi import Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from random import randint
from database import *
import oauth2

router = APIRouter(
    tags=["admin tools"]
)


class LessonPostModel(BaseModel):
    class_id: int
    day: int
    subject_1_id: int
    subject_2_id: int
    subject_3_id: int
    subject_4_id: int
    subject_5_id: int
    subject_6_id: int
    teacher_id: str

    class Config:
        orm_mode = True


@router.get("/api/admintools/schedule")
def create_schedule(db: Session = Depends(get_db)):
    class_id = 1
    teacher_id = "90b8df65-0c52-4c8c-a02a-980d16e34f69"
    subject_id = 0

    for i in range(1, 8):
        for j in range(1, 7):
            subject_id = randint(1, 10)
            new_lesson = Lesson(class_id=class_id, day=i, lesson_num=j, teacher_id=teacher_id, subject_id=subject_id)
            db.add(new_lesson)
            db.commit()
            db.refresh(new_lesson)

    return "schedule created"
