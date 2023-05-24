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


@router.post("/api/admintools/lesson", )
def create_lesson(lesson: LessonPostModel, db: Session = Depends(get_db),
                  current_user: str = Depends(oauth2.get_current_user)):
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson


@router.get("/api/admintools/schedule")
def create_schedule(db: Session = Depends(get_db)):
    class_id = 1
    day = 1
    subject_ids = [0, 0, 0, 0, 0, 0]
    teacher_id = "90b8df65-0c52-4c8c-a02a-980d16e34f69"

    for i in range(1, 8):
        for j in range(0, 6):
            subject_ids[j] = randint(1, 10)

        day = i
        new_lesson = Lesson(class_id=class_id, day=day, subject_1_id=subject_ids[0], subject_2_id=subject_ids[1],
                            subject_3_id=subject_ids[2], subject_4_id=subject_ids[3], subject_5_id=subject_ids[4],
                            subject_6_id=subject_ids[5], teacher_id=teacher_id)
        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)

    return "schedule created"
