from abc import ABC, abstractmethod
from domain.model import UserRegister,User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, user: UserRegister):
        pass

    @abstractmethod
    async def get_by_person_id(self, person_id: str) -> User | None:
        pass
    
    @abstractmethod
    async def find_by_phone_number(self, phone_number: str) -> UserRegister | None:
        pass
    @abstractmethod
    async def get_max_numeric_for_year(self, year_suffix: str) -> int | None:
        pass