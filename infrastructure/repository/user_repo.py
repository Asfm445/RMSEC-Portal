from domain.interfaces.user_repo import UserRepositoryInterface
from domain.model import UserRegister, User
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.dto.user_dto import from_user_register_to_person, from_db_person_to_user
from sqlalchemy import select, func, cast, Integer
from infrastructure.models.model import Person, Student, Teacher, Admin, Grade  # <-- import new models
from sqlalchemy.orm import selectinload


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: UserRegister):
        person = from_user_register_to_person(user)
        try:
            self.db.add(person)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False

    async def get_by_person_id(self, person_id: str) -> User | None:

        result = await self.db.execute(
            select(Person)
            .options(
                selectinload(Person.student),
                selectinload(Person.teacher),
                selectinload(Person.admin)
            )
            .filter(Person.person_id == person_id)
        )

        person = result.scalar_one_or_none()
        if person:
            return from_db_person_to_user(person)  # should now detect student/teacher/admin
        return None
    
    async def get_by_id(self, id: int) -> User | None:
        result = await self.db.execute(
            select(Person)
            .options(
                selectinload(Person.student).selectinload(Student.grades),
                selectinload(Person.teacher),
                selectinload(Person.admin)
            )
            .filter(Person.id == id)
        )


        person = result.scalar_one_or_none()

        if person:
            return from_db_person_to_user(person) 
        # should now detect student/teacher/admin
        return None

    async def get_max_numeric_for_year(self, year_suffix: str) -> int | None:
        result = await self.db.execute(
            select(func.max(cast(func.split_part(Person.person_id, '/', 1), Integer)))
            .filter(func.split_part(Person.person_id, '/', 2) == year_suffix)
        )
        return result.scalar_one_or_none()

    async def find_by_phone_number(self, phone_number: str) -> UserRegister | None:
        result = await self.db.execute(
            select(Person).filter(Person.phone_number == phone_number)
        )
        person = result.scalar_one_or_none()
        if person:
            return UserRegister(
                name=person.name,
                phone_number=person.phone_number,
                password=person.hashed_password,
                person_id=person.person_id
            )
        return None

    async def add_teacher(self, person_id: str):
        self.db.add(Teacher(person_id=person_id))
        await self.db.commit()
        return True

    async def add_admin(self, person_id: str):
        self.db.add(Admin(person_id=person_id))
        await self.db.commit()
        return True

        
    async def add_student_to_grade(self, person_id: str, grade_no: int, year: int):
        # 1. Get the person first (by string person_id)
        result = await self.db.execute(select(Person).filter(Person.id == person_id))
        person = result.scalar_one_or_none()
        if not person:
            raise Exception("Person not found")

        # 2. Get the student with grades eagerly loaded
        result = await self.db.execute(
            select(Student).options(selectinload(Student.grades)).filter(Student.person_id == person.id)
        )
        student = result.scalar_one_or_none()
        if not student:
            student = Student(person_id=person.id)
            self.db.add(student)
            await self.db.flush()  # flush to get student in session

        # 3. Get or create grade
        result = await self.db.execute(
            select(Grade).filter(Grade.grade_No == grade_no, Grade.year == year)
        )
        grade = result.scalar_one_or_none()
        if not grade:
            grade = Grade(grade_No=grade_no, year=year)
            self.db.add(grade)
            await self.db.flush()  # flush to get grade in session

        # 4. Avoid duplicate association safely
        if grade not in student.grades:  # now grades are loaded, no lazy IO
            student.grades.append(grade)

        await self.db.commit()
        return True
