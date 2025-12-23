from abc import ABC, abstractmethod
from domain.model import UserRegister, User


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def create(self, user: UserRegister) -> bool:
        """
        Create a new Person record.
        Returns True if success, False if failure.
        """

    @abstractmethod
    async def get_by_person_id(self, person_id: str) -> User | None:
        """
        Return a User domain object with role (student/teacher/admin) attached.
        Return None if not found.
        """

    @abstractmethod
    async def get_max_numeric_for_year(self, year_suffix: str) -> int | None:
        """
        Extract last numeric ID for a given year (person_id formatted as "num/yy")
        """

    @abstractmethod
    async def find_by_phone_number(self, phone_number: str) -> UserRegister | None:
        """
        Search Person by phone number for registration verification.
        Returns UserRegister or None.
        """

    @abstractmethod
    async def get_by_id(self, id: int) -> User | None:  
        pass

    @abstractmethod
    async def check_user_exist(self, person_id: str) -> bool:
        pass

    @abstractmethod
    async def check_phone_number_exist(self, phone_number: str) -> bool:
        pass

    @abstractmethod
    async def get_user_roles(self, person_id: str) -> list[str] | None:
        pass
