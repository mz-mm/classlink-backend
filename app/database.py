import uuid
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Sequence
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text, false
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

# Each user type like parent or teacher or student should have a username prefix, like teachers will have a prefix if t in their username


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
    first_parent_id = Column(String, ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
    second_parent_id = Column(String, ForeignKey("parents.id", ondelete="CASCADE"))
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
    
    # Parents that have children will need to have a separate account as parent account
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
    class_grade = Column(Integer, nullable=False) # Meaning class like grade 1 to 11
    class_name = Column(String, nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    sector = Column(Enum("az", "ru", name="sector"), nullable=False)



class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False)
    day = Column(Integer, nullable=False)
    lesson_num = Column(Integer, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    subject = relationship("Subject")


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
    status = Column(Boolean, nullable=False, default=False) # True if present, False otherwise
    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))



class SubjectGrade(Base):
    __tablename__ = "subject_grades"

    id = Column(Integer, primary_key=True, nullable=False)
    student_id = Column(String, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    grade = Column(Integer, nullable=False)
    teacher_id = Column(String, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    date = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    student = relationship("Student")



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


# Before sending th user their schedule, the api will first check if there is any school event on that day on time block, if so that it will place the event next or overidde the schedule for that day/
# for example, if there is no school day, wich will be an event in the schedule_event table, it will simply return a empty lesson for today instead of the ussal response
# class SchoolEvents(Base):
#     _tablename = "school_events"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    from_id = Column(String, nullable=False)
    to_id = Column(String, nullable=False)

    date = Column(TIMESTAMP, nullable=False)    
