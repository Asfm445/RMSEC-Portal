from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserRegister:
    name: str
    phone_number: str
    password: str
    person_id: str | None = None


@dataclass
class UserLogin:
    id: str
    password: str


@dataclass
class User:
    id: int
    person_id: str
    name: str
    phone_number: str
    registered_at: datetime
    hashed_password: str
    student: Optional[bool] = None  # True if user has a Student record
    teacher: Optional[bool] = None  # True if user has a Teacher record
    admin: Optional[bool] = None    # True if user has an Admin record
