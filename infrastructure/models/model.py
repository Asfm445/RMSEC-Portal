from infrastructure.db.session import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

class RoleType(PyEnum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(SQLEnum(RoleType, name="role_type"), nullable=False, index=True)
    taken_at = Column(DateTime, default=datetime.now)
    ended_at = Column(DateTime, nullable=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), index=True)

    person = relationship("Person", back_populates="roles")

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    registered_at = Column(DateTime, default=datetime.now)  # remove () so default is called at insert
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    person_id= Column(String, unique=True, index=True)
    # one-to-many for Role history (if you want history)
    roles = relationship("Role", back_populates="person", cascade="all, delete-orphan")

    # one-to-one relationships to specific profiles
    student = relationship("Student", back_populates="person", uselist=False)
    teacher = relationship("Teacher", back_populates="person", uselist=False)
    admin = relationship("Admin", back_populates="person", uselist=False)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)

    person = relationship("Person", back_populates="student", uselist=False)

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey('persons.id', ondelete="CASCADE"), unique=True, index=True)

    person = relationship("Person", back_populates="teacher", uselist=False)

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
    grade_No=Column(Integer, index=True)
    Total_point=Column(Float, nullable=True)

    role_id = Column(Integer, ForeignKey('roles.id', ondelete="CASCADE"), index=True)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    grade_id = Column(Integer, ForeignKey('grades.id', ondelete="CASCADE"), index=True)
