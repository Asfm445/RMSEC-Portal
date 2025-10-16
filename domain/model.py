from dataclasses import dataclass

from datetime import datetime
from typing import List, Optional
from enum import Enum


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


# If you want to mirror your RoleType enum
class RoleType(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

@dataclass
class RoleData:
    id: int
    type_id: RoleType
    taken_at: datetime
    ended_at: Optional[datetime] = None

@dataclass
class User:
    id: int
    person_id: str
    name: str
    phone_number: str
    registered_at: datetime
    hashed_password: str 
    roles: List[RoleData]

    