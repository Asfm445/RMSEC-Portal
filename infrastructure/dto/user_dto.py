from domain.model import UserRegister
from infrastructure.models.model import Person


def from_user_register_to_person(user: UserRegister)->Person:
    return Person(
        name=user.name,
        hashed_password=user.password,
        phone_number=user.phone_number

    )
