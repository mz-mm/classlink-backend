from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db, Lesson
import oauth2
from schemas import lessonScheme


router = APIRouter(
    tags=["Lesson"]
)

def sort_lessons(lessons):
    sorted_lessons = []
    lesson_num = 1
    day = 1

    for _ in range(36):
        for lesson in lessons:
            if lesson.day == day and lesson.lesson_num == lesson_num:
                sorted_lessons.append(lesson)
                day += 1
                if day > 6:
                    day = 1
                    lesson_num += 1
                break

    return sorted_lessons

@router.get("/api/schedule", response_model=List[lessonScheme.LessonResponsModel])
def get_lessons(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    lessons = db.query(Lesson).filter(Lesson.class_id == current_user.class_id).all()

    lessons = sort_lessons(lessons)

    return lessons


@router.get("/api/schedule/{id}", response_model=List[lessonScheme.LessonResponsModel])
def get_lessons(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    lessons = db.query(Lesson).filter(Lesson.class_id == current_user.class_id)
    lessons = lessons.filter(Lesson.day == id).all()

    return lessons