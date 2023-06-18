from fastapi import Depends, APIRouter, HTTPException, status
from schemas.attendanceScheme import AttendanceModel_R, LessonDetailModel_P
from database import Teacher, Student, Lesson, get_db, Attendance
from rate_limit import rate_limited, Request
from util import getCurrentDay
from sqlalchemy.orm import Session
from sqlalchemy import asc, extract
from typing import List
import oauth2

router = APIRouter(
    tags=["Teacher Attendance"]
)

@router.post("/api/teacher/attendance", response_model=List[AttendanceModel_R])
@rate_limited(max_calls=100, time_frame=60)
def mark_attendance(request: Request, lessonDetail: LessonDetailModel_P, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    day = 3 # ONLY FOR DEVELOPMENT

    students = []
    # uncomment for production
    # day = getCurrentDay(lessonDetail.day)

    teacher = db.query(Teacher).filter(Teacher.id == current_user.id).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prohibited request")

    attendance:Attendance = db.query(Attendance).filter(
        Attendance.teacher_id == teacher.id,
        extract('year', Attendance.date) == lessonDetail.year,
        extract('month', Attendance.date) == lessonDetail.month,
        extract('day', Attendance.date) == lessonDetail.day,
        Attendance.day == day,
        Attendance.lesson_num == lessonDetail.current_lesson
    ).all()

    if attendance:
        for student in attendance:
            query = db.query(Student).filter(Student.id == student.student_id).first()
            students.append(query)

    else:
        attendance = db.query(Student).join(Lesson, Student.class_id == Lesson.class_id).filter(
        Lesson.day == day, Lesson.lesson_num == lessonDetail.current_lesson,
        Lesson.teacher_id == current_user.id).order_by(asc(Student.full_name)).all()

        if not attendance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ваши уроки еще не начались или уже закончились")
        
        for student in attendance:
            new_attendance = Attendance(student_id=student.id, teacher_id=teacher.id, lesson_num=lessonDetail.current_lesson, day=day)
            db.add(new_attendance)
            db.commit()
            db.refresh(new_attendance)

            query = db.query(Student).filter(Student.id == new_attendance.student_id).first()
            students.append(query)
        


    response_data = [
        AttendanceModel_R(id=student.id, full_name=student.full_name) for student in students
    ]

    return response_data