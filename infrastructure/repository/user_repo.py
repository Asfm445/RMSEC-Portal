from domain.interfaces.user_repo import UserRepositoryInterface
from domain.model import UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.dto.user_dto import from_user_register_to_person, from_db_person_to_user
from sqlalchemy import select, func, cast, Integer
from infrastructure.models.model import Person
from sqlalchemy.orm import selectinload
from domain.model import User


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

    async def get_by_person_id(self, person_id: str) -> User | None:
        result = await self.db.execute(
            select(Person)
            .options(selectinload(Person.roles))  # Eagerly load roles
            .filter(Person.person_id == person_id)
        )
        person = result.scalar_one_or_none()
        if person:
            return from_db_person_to_user(person)
        return None
    async def get_max_numeric_for_year(self, year_suffix: str) -> int | None:
        """
        For person_id formatted as "<number>/<yy>", return max(number) for given yy.
        Uses Postgres split_part(person_id, '/', 1) cast to integer.
        """
        result = await self.db.execute(
            select(func.max(cast(func.split_part(Person.person_id, '/', 1), Integer)))
            .filter(func.split_part(Person.person_id, '/', 2) == year_suffix)
        )
        max_num = result.scalar_one_or_none()
        return max_num
    
    async def find_by_phone_number(self, phone_number: str) -> UserRegister | None:
        result = await self.db.execute(
            select(Person).filter(Person.phone_number == phone_number)
        )
        person = result.scalar_one_or_none() .options(selectinload(Person.roles))
        if person:
            return UserRegister(
                name=person.name,
                phone_number=person.phone_number,
                password=person.hashed_password,
                person_id=person.person_id
            )
        return None