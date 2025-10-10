from dataclasses import dataclass




@dataclass
class UserRegister:
    name: str
    phone_number: str
    password: str
    