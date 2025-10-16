from domain.interfaces.jwt_service import JWTServiceInterface
from datetime import datetime, timedelta, timezone
from domain.exceptions import BadRequestError
from jose import ExpiredSignatureError, JWTError, jwt


class JwtService(JWTServiceInterface):
    def __init__(
        self,
        SECRET_KEY: str,
        ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES: int,
        REFRESH_TOKEN_EXPIRE_HOURS: int,
    ):
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_HOURS = REFRESH_TOKEN_EXPIRE_HOURS

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict) -> str:  
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=self.REFRESH_TOKEN_EXPIRE_HOURS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise BadRequestError("Token has expired")
        except JWTError:
            raise BadRequestError("Invalid token")
