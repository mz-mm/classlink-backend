from pydantic import BaseModel

class AttendanceModel_R(BaseModel):
    id: str
    full_name: str

    class Config:
        orm_mode = True


class LessonDetailModel_P(BaseModel):
    current_day: str
    current_lesson: int
    year: int
    month: int
    day: int