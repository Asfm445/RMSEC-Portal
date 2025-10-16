from domain.model import UserRegister
from infrastructure.models.model import Person
from domain.model import User, RoleData


def from_user_register_to_person(user: UserRegister)->Person:
    return Person(
        name=user.name,
        hashed_password=user.password,
        phone_number=user.phone_number,
        person_id=user.person_id

    )

def from_db_person_to_user(person: Person) -> User:
    roles = [
        RoleData(
            id=role.id,
            type_id=role.type_id,
            taken_at=role.taken_at,
            ended_at=role.ended_at
        )
        for role in person.roles
    ]
    return User(
        id=person.id,
        person_id=person.person_id,
        name=person.name,
        phone_number=person.phone_number,
        registered_at=person.registered_at,
        hashed_password=person.hashed_password,
        roles=roles
    )
