from pydantic import BaseModel



class UserRegisterSchema(BaseModel):
    name: str
    password: str
    phone_number: str