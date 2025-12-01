from infrastructure.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime

# Association table for many-to-many between students and grades
student_grade_association = Table(
    'student_grades',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete="CASCADE"), primary_key=True),
    Column('grade_id', Integer, ForeignKey('grades.id', ondelete="CASCADE"), primary_key=True)
)


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    registered_at = Column(DateTime, default=datetime.now)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    person_id = Column(String, unique=True, index=True)

    # One-to-one relationships to specific profiles
    student = relationship("Student", back_populates="person", uselist=False)
    teacher = relationship("Teacher", back_populates="person", uselist=False)
    admin = relationship("Admin", back_populates="person", uselist=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)
    approved = Column(Boolean, default=False)

    person = relationship("Person", back_populates="student", uselist=False)
    grades = relationship(
        "Grade",
        secondary=student_grade_association,
        back_populates="students",
        uselist=True
    )


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)
    approved = Column(Boolean, default=False)

    person = relationship("Person", back_populates="teacher", uselist=False)
    subjects = relationship("Subject", back_populates="teacher", uselist=True)  # One teacher -> many subjects


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)

    person = relationship("Person", back_populates="admin", uselist=False)


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    grade_No = Column(Integer, index=True)
    total_point = Column(Float, nullable=True)

    subjects = relationship("Subject", back_populates="grade", uselist=True)  # One grade -> many subjects
    students = relationship(
        "Student",
        secondary=student_grade_association,
        back_populates="grades",
        uselist=True
    )


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    teacher_id = Column(Integer, ForeignKey('teachers.id'), index=True)
    grade_id = Column(Integer, ForeignKey('grades.id', ondelete="CASCADE"), index=True)

    teacher = relationship("Teacher", back_populates="subjects", uselist=False)
    grade = relationship("Grade", back_populates="subjects", uselist=False)
