from typing import Optional, List, Union
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session 
from database import *
import oauth2
from datetime import datetime


router = APIRouter(
    tags=["Teacher Grading"]
)

class StudentModel(BaseModel):
    id: str
    full_name: str

class TeacherModel(BaseModel):
    id: str
    full_name: str


class GradeModel(BaseModel):
    grade: int
    subject: int
    student: StudentModel
    teacher: TeacherModel

class GradeReponsModel(BaseModel):
    id: int
    grade: int
    subject: int
    student: StudentModel
    teacher: TeacherModel
    date: datetime




@router.get("/api/teacher/grade", response_model=List[GradeReponsModel])
def set_grade(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    teacher = db.query(Teacher).filter(Teacher.id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

    student = db.query(Student).join(Lesson, Student.class_id == Lesson.class_id).filter(Lesson.teacher_id == current_user.id).all()

    response_data = [
        GradeReponsModel( id=student.id, full_name=student.full_name,) for student in student
            # Map other fields accordingly
    ]

    return response_data




@router.post("/api/teacher/grade")
def mark_grade(attendance: GradeModel, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    teacher = db.query(Teacher).filter(Teacher.id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

    new_attendance = Attendance(student_id=attendance.id, teacher_id=teacher.id, status=attendance.status ,late=attendance.late)
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance
