from infrastructure.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    registered_at = Column(DateTime, default=datetime.now)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)



class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)
    grade_no = Column(Integer, index=True)
    year = Column(Integer, index=True)
    approved = Column(Boolean, default=False)



class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)
    approved = Column(Boolean, default=False)
    grade_no = Column(Integer, index=True)



class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    position = Column(String, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)

    


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    grade_no = Column(Integer, index=True)

    


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    year = Column(Integer, index=True)
    grade_no = Column(Integer, index=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), index=True)

