from typing import Optional, List, Union
from fastapi import Depends, APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import asc
import database
import oauth2

router = APIRouter(
    tags=["Teacher Attendance"]
)


class StudentAttendanceResponsModel(BaseModel):
    id: str
    full_name: str

    class Config:
        orm_mode = True


# @router.get("/api/teacher/attendance", response_model=List[StudentAttendanceResponsModel])
# def get_attendance(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

#     teacher = db.query(Teacher).filter(Teacher.id == current_user.id).first()
#     if not teacher:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

#     student = db.query(Student).filter(Lesson.teacher_id == current_user.id).all()

#     response_data = [
#         StudentAttendanceResponsModel( id=student.id, full_name=student.full_name,) for student in student
#             # Map other fields accordingly
#     ]

#     return response_data


# @router.post("/api/teacher/attendance")
# def mark_attendance(attendance: StudentAttendanceModel, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

#     teacher = db.query(Teacher).filter(Teacher.id == current_user.id).first()
#     if not teacher:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

#     new_attendance = Attendance(student_id=attendance.id, teacher_id=teacher.id, status=attendance.status ,late=attendance.late)
#     db.add(new_attendance)
#     db.commit()
#     db.refresh(new_attendance)

#     return new_attendance


class StudentAttendanceModel(BaseModel):
    current_day: str
    current_lesson: int
    date: str


@router.post("/api/teacher/attendance", response_model=List[StudentAttendanceResponsModel])
def mark_attendance(attendance: StudentAttendanceModel, db: Session = Depends(database.get_db),
                    current_user: str = Depends(oauth2.get_current_user)):
    day = 3

    # if attendance.current_day == "Tuesday":
    #     day = 2
    # elif attendance.current_day == "Wednesday":
    #     day = 3
    # elif attendance.current_day == "Thursday":
    #     day = 4
    # elif attendance.current_day == "Friday":
    #     day = 5
    # elif attendance.current_day == "Saturday":
    #     day = 6

    teacher = db.query(database.Teacher).filter(database.Teacher.id == current_user.id).first()

    if not teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

    student = db.query(database.Student). \
        join(database.Lesson, database.Student.class_id == database.Lesson.class_id).filter(
        database.Lesson.day == day,
        database.Lesson.lesson_num == attendance.current_lesson,
        database.Lesson.teacher_id == current_user.id
    ).order_by(asc(database.Student.full_name)).all()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Ваши уроки еще не начались или уже закончились")

    response_data = [
        StudentAttendanceResponsModel(id=student.id, full_name=student.full_name) for student in student
    ]

    return response_data
