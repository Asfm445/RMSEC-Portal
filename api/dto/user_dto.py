from api.schema.user_schema import UserRegisterSchema, UserLogin as UserLoginSchema
from domain.model import UserRegister, UserLogin


def from_user_register_schema_to_model(user_schema: UserRegisterSchema) -> UserRegister:
    return UserRegister(
        name=user_schema.name,
        phone_number=user_schema.phone_number,
        password=user_schema.password
    )

def from_user_login_schema_to_model(user_schema: UserLoginSchema) -> UserLogin:
    return UserLogin(id= user_schema.id, password=user_schema.password)