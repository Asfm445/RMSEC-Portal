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
    async def add_student_to_grade(self, person_id: str, grade_no: int, year: int):
        pass

    @abstractmethod
    async def add_teacher(self, person_id: str) -> bool:
        """
        Assign user role: teacher
        Since only one role exists per person type, create matching record.
        Returns True if assigned, False if person not found or invalid role.
        """

    @abstractmethod
    async def add_admin(self, person_id: str) -> bool:
        """
        Assign user role: admin
        Since only one role exists per person type, create matching record.
        Returns True if assigned, False if person not found or invalid role.
        """
    @abstractmethod
    async def get_by_id(self, id: int) -> User | None:  
        pass
