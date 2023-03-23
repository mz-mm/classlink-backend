from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
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


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    class_id = Column(String, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)

    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)

    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_subscription_fee = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    last_subscription_fee = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, nullable=False)
    class_grade = Column(Integer, nullable=False)
    class_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, nullable=False)
    class_id = Column(String, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    day = Column(Integer, nullable=False)
    lesson_num = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    late = Column(Integer, nullable=True)


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)


class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(TIMESTAMP, nullable=False)
    class_id = Column(String, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(TIMESTAMP, nullable=False)
    class_id = Column(String, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
