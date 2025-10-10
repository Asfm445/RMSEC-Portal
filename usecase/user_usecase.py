from domain.model import UserRegister
from domain.interfaces.user_repo import UserRepositoryInterface
from domain.interfaces.password_service import PasswordServiceInterface


class UserUseCase:
    def __init__(self, user_repo: UserRepositoryInterface, pass_service: PasswordServiceInterface):
        self.user_repo=user_repo
        self.pass_service=pass_service
    
    async def register_user(self, user: UserRegister):
        user.password=self.pass_service.hash_password(user.password)
        if self.user_repo.create(user):
            return {"message":" user registered successfully"}
        return {"message":"user registration failed"}
        
