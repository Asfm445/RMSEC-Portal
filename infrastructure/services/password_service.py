from passlib.context import CryptContext
from domain.interfaces.password_service import PasswordServiceInterface


class PasswordService(PasswordServiceInterface):
    def __init__(self):
        # use argon2 (no 72-byte bcrypt limit)
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)