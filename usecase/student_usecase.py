from domain.interfaces.student_repo import StudentRepositoryInterface
from domain.exceptions import BadRequestError, NotFoundError
from datetime import date
from domain.interfaces.user_repo import UserRepositoryInterface

class StudentUseCase:
    def __init__(self, student_repo: StudentRepositoryInterface, user_repo: UserRepositoryInterface):
        self.student_repo = student_repo    
        self.user_repo = user_repo

    async def apply_student(self, person_id: int, grade_no: int):
        if grade_no < 1 or grade_no > 12:
            raise BadRequestError("Invalid grade number")
        # Ensure person_id is an integer
        person_id = int(person_id)
        user = await self.user_repo.get_by_id(person_id)
        if not user:
            raise NotFoundError("User Not Found")

        grade = await self.student_repo.check_grade(grade_no)
        if not grade:
            raise BadRequestError("grade application not started yet")
        
        g = date.today()
        eth_year = g.year - 7 if (g.month > 9 or (g.month == 9 and g.day >= 11)) else g.year - 8

        success=await self.student_repo.create_new_student(person_id, grade_no, eth_year)
        if not success:
            raise BadRequestError("Failed to create student record")
        return {"message": f"User {person_id} has successfully applied as a student for grade {grade_no}. wait for approval"}


       