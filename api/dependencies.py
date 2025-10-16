
from infrastructure.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repository.user_repo import UserRepository
from infrastructure.services.password_service import PasswordService
from usecase.user_usecase import UserUseCase
from infrastructure.services.jwt_service import JwtService
from fastapi import Depends
import os


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_HOURS = int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS"))



def get_usecase(db: AsyncSession = Depends(get_db))-> UserUseCase:
    pass_service=PasswordService()
    user_repo=UserRepository(db)
    jwt_service=JwtService(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_HOURS)

    return UserUseCase(user_repo, pass_service,jwt_service)


