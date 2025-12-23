from abc import ABC, abstractmethod



class StudentRepositoryInterface(ABC):
    @abstractmethod
    def check_grade(self, grade_no: int):
        pass
    
    @abstractmethod
    def create_new_student(self, person_id: str, grade_no: int, year: int):
        pass
