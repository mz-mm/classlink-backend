from typing import Optional, List, Union
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session 
from database import *
import oauth2


router = APIRouter(
    tags=["Teacher Attendance"]
)

class StudentAttendanceModel(BaseModel):
    id: str
    status: bool = False
    late: Optional[int]

class StudentAttendanceResponsModel(BaseModel):
    id: str
    full_name: str

    class Config:
        orm_mode = True


@router.get("/api/teacher/attendance", response_model=List[StudentAttendanceResponsModel])
def get_attendance(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    teacher = db.query(Teacher).filter(Teacher.id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

    student = db.query(Student).filter(Lesson.teacher_id == current_user.id).all()

    response_data = [
        StudentAttendanceResponsModel( id=student.id, full_name=student.full_name,) for student in student
            # Map other fields accordingly
    ]

    return response_data


@router.post("/api/teacher/attendance")
def mark_attendance(attendance: StudentAttendanceModel, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    teacher = db.query(Teacher).filter(Teacher.id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

    new_attendance = Attendance(student_id=attendance.id, teacher_id=teacher.id, status=attendance.status ,late=attendance.late)
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance
