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
    class_id = 7
    teacher_ids = [
        "067c5976-daca-42a5-82d8-8b6951193c8b",
        "129b097b-e509-42be-9557-ec2e69757298",
        "7b6cf347-a225-416d-b2ba-b511177efc73",
        "8ab571fd-217b-416c-842f-ca94302fc5c1",
        "95f11c1e-d960-4265-8e25-e0322de60af1",
        "a13aa2b9-146d-4f62-bf34-963488ab58b9",
        "a9fe3759-0fa0-4833-9d5c-74cab464ce2e",
        "a9fe3759-0fa0-4833-9d5c-74cab464ce2e",
        "c8c36ed0-3d64-4ae8-bd40-d96f39a1c2c7"
    ]
    subject_id = 0

    for i in range(1, 7):
        for j in range(1, 7):
            subject_id = randint(1, 9)
            new_lesson = Lesson(class_id=class_id, day=i, lesson_num=j, teacher_id=teacher_ids[subject_id-1], subject_id=subject_id)
            db.add(new_lesson)
            db.commit()
            db.refresh(new_lesson)

    return "schedule created"
