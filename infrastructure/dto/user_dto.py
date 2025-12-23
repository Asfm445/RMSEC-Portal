from domain.model import UserRegister
from infrastructure.models.model import Person
from domain.model import User


def from_user_register_to_person(user: UserRegister) -> Person:
    """
    Map UserRegister domain model to Person DB model
    """
    return Person(
        name=user.name,
        hashed_password=user.password,
        phone_number=user.phone_number,
        person_id=user.person_id
    )


def from_db_person_to_user(person: Person) -> User:
    """
    Map Person DB model to User domain model.
    Includes student, teacher, and admin relationships for role detection.
    """
    return User(
        id=person.id,
        person_id=person.person_id,
        name=person.name,
        phone_number=person.phone_number,
        registered_at=person.registered_at,
        hashed_password=person.hashed_password,
    )
