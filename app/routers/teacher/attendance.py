from typing import Optional, List, Union
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session 
from database import *
import oauth2


router = APIRouter(
    tags=["Teacher Attendance"]
)


class StudentAttendanceResponseModel(BaseModel):
    full_name: str

@router.get("/api/attendance", response_model=List[StudentAttendanceResponseModel])
def mark_attendance(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    user = db.query(Teacher).filter(Teacher.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

    attendance = db.query(Student).join(Lesson, Student.class_id == Lesson.class_id).filter(Lesson.teacher_id == current_user.id).all()

    response_data = [
        StudentAttendanceResponseModel(
            full_name=student.full_name,
            # Map other fields accordingly
        )
        for student in attendance
    ]

    return response_data


@router.post("/api/attendence")
def mark_attendance(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    return {"result":"mark attendence"}
