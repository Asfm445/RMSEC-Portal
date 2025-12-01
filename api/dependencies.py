
from infrastructure.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.repository.user_repo import UserRepository
from infrastructure.services.password_service import PasswordService
from usecase.user_usecase import UserUseCase
from infrastructure.services.jwt_service import JwtService
from fastapi import Depends, HTTPException
from jose import JWTError
import os
from fastapi.security import OAuth2PasswordBearer

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_HOURS = int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")



def get_usecase(db: AsyncSession = Depends(get_db))-> UserUseCase:
    pass_service=PasswordService()
    user_repo=UserRepository(db)
    jwt_service=JwtService(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_HOURS)

    return UserUseCase(user_repo, pass_service,jwt_service)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_usecase: UserUseCase = Depends(get_usecase),
):
    try:
        payload = user_usecase.jwt_service.decode_token(token)  # only one value
        print("++++++++++++++++++++++++++++++++++++++++++++++++here in dependencies++++++++++++++++++++++")
        print(payload)
        if not payload or "sub" not in payload:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return payload



