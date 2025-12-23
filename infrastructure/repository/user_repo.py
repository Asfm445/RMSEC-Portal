from domain.interfaces.user_repo import UserRepositoryInterface
from domain.model import UserRegister, User
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.dto.user_dto import from_user_register_to_person, from_db_person_to_user
from sqlalchemy import select, func, cast, Integer, exists
from infrastructure.models.model import Person, Student, Teacher, Admin, Grade  # <-- import new models
from sqlalchemy.orm import selectinload


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserRegister):
        person = from_user_register_to_person(user)
        try:
            self.db.add(person)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False
    
    async def check_user_exist(self, person_id: str) -> bool:
        result = await self.db.execute(
            select(exists().where(Person.person_id == person_id))
        )

        return result.scalar_one_or_none()

    async def check_phone_number_exist(self, phone_number: str) -> bool:
        result = await self.db.execute(
            select(exists().where(Person.phone_number == phone_number))
        )   

        return result.scalar_one_or_none()
    
    async def get_user_roles(self, person_id: str) -> list[str] | None:
        student = await self.db.execute(
            select(exists().where(Student.person_id == person_id))
        )

        teacher = await self.db.execute(
            select(exists().where(Teacher.person_id == person_id))
        )

        admin = await self.db.execute(
            select(exists().where(Admin.person_id == person_id))
        )
        ans=[]
        if student.scalar_one_or_none():
            ans.append("student")
        if teacher.scalar_one_or_none():
            ans.append("teacher")
        if admin.scalar_one_or_none():
            ans.append("admin")
        return ans

    async def get_by_person_id(self, person_id: str) -> User | None:

        result = await self.db.execute(
            select(Person)
            .filter(Person.person_id == person_id)
        )

        person = result.scalar_one_or_none()
        if person:
            return from_db_person_to_user(person)  # should now detect student/teacher/admin
        return None
    
    async def get_by_id(self, id: int) -> User | None:
        result = await self.db.execute(
            select(Person)
            .filter(Person.id == id)
        )


        person = result.scalar_one_or_none()

        if person:
            return from_db_person_to_user(person) 
        # should now detect student/teacher/admin
        return None

    async def get_max_numeric_for_year(self, year_suffix: str) -> int | None:
        result = await self.db.execute(
            select(func.max(cast(func.split_part(Person.person_id, '/', 1), Integer)))
            .filter(func.split_part(Person.person_id, '/', 2) == year_suffix)
        )
        return result.scalar_one_or_none()

    async def find_by_phone_number(self, phone_number: str) -> UserRegister | None:
        result = await self.db.execute(
            select(Person).filter(Person.phone_number == phone_number)
        )
        person = result.scalar_one_or_none()
        if person:
            return UserRegister(
                name=person.name,
                phone_number=person.phone_number,
                password=person.hashed_password,
                person_id=person.person_id
            )
        return None
   