
from infrastructure.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repository.user_repo import UserRepository
from infrastructure.services.password_service import PasswordService
from usecase.user_usecase import UserUseCase
from fastapi import Depends


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


def get_usecase(db: AsyncSession = Depends(get_db))-> UserUseCase:
    pass_service=PasswordService()
    user_repo=UserRepository(db)

    return UserUseCase(user_repo, pass_service)


