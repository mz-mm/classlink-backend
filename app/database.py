import uuid
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Sequence
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Admin(Base):
    __tablename__ = "admins"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), server_default=text('uuid_generate_v4()'), unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))



class Student(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), server_default=text('uuid_generate_v4()'), unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    sector = Column(Enum("az", "ru", name="sector"), nullable=False)

    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))



class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(String, primary_key=True, default=str(uuid.uuid4()), server_default=text('uuid_generate_v4()'), unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_subscription_fee = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) # Parents will have to pay for all their children together



class Teacher(Base):
    __tablename__ = "teachers"


    id = Column(String, primary_key=True, default=str(uuid.uuid4()), server_default=text('uuid_generate_v4()'), unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    sector = Column(Enum("az", "ru", name="sector"), nullable=False)

    last_subscription_fee = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, nullable=False)
    class_grade = Column(Integer, nullable=False)
    class_name = Column(String, nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    sector = Column(Enum("az", "ru", name="sector"), nullable=False)



class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    day = Column(Integer, nullable=False)

    subject_1_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    subject_2_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    subject_3_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    subject_4_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    subject_5_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    subject_6_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    subject_1 = relationship("Subject", foreign_keys=[subject_1_id], lazy='subquery', uselist=False)
    subject_2 = relationship("Subject", foreign_keys=[subject_2_id], lazy='subquery', uselist=False)
    subject_3 = relationship("Subject", foreign_keys=[subject_3_id], lazy='subquery', uselist=False)
    subject_4 = relationship("Subject", foreign_keys=[subject_4_id], lazy='subquery', uselist=False)
    subject_5 = relationship("Subject", foreign_keys=[subject_5_id], lazy='subquery', uselist=False)
    subject_6 = relationship("Subject", foreign_keys=[subject_6_id], lazy='subquery', uselist=False)


class Subject(Base):
    __tablename__ = "subjects"
    # there also should be a null subject or a emtpy subject for example if in some days there only 5 or less lessons
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)



class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    late = Column(Integer, nullable=True)
    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class SubjectGrade(Base):
    __tablename__ = "subject_grades"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    grade = Column(Integer, nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    due_date = Column(TIMESTAMP, nullable=False)



class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    date = Column(TIMESTAMP, nullable=False)



# ---- NOT READY FEATURE ----
# class Message(Base):
    # __tablename__ = "messages"
# 
    # id = Column(Integer, primary_key=True, nullable=False)
    # title = Column(String, nullable=False)
    # description = Column(String, nullable=True)
# 
    # date = Column(TIMESTAMP, nullable=False)    
