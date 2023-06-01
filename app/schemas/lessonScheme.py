from pydantic import BaseModel


class SubjectResponsModel(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        orm_mode = True


class LessonResponsModel(BaseModel):
    id: int
    subject: SubjectResponsModel

    class Config:
        orm_mode = True