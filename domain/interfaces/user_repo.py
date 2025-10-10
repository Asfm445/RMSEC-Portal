from abc import ABC, abstractmethod
from domain.model import UserRegister


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, user: UserRegister) -> bool:
        pass