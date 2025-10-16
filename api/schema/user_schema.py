from pydantic import BaseModel



class UserRegisterSchema(BaseModel):
    name: str
    password: str
    phone_number: str

class UserLogin(BaseModel):
    id: str
    password: str