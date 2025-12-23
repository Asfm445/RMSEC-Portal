from domain.interfaces.student_repo import StudentRepositoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.models.model import Grade, Student
from sqlalchemy import select, exists

class StudentRepository(StudentRepositoryInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_grade(self, grade_no: int) -> bool:
        result = await self.db.execute(
            select(exists().where(Grade.grade_no == grade_no))
        )
        return result.scalar_one_or_none()
    
    async def create_new_student(self, person_id: int, grade_no: int, year: int):
        student = Student(person_id=person_id, grade_no=grade_no, year=year)
        self.db.add(student)
        await self.db.commit()
        return True
    