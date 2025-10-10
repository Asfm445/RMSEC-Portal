from domain.interfaces.user_repo import UserRepositoryInterface
from domain.model import UserRegister
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.dto.user_dto import from_user_register_to_person

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserRegister) -> bool:
        person=from_user_register_to_person(user)
        # Implementation to create a user in the database
        try:
            self.db.add(person)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False