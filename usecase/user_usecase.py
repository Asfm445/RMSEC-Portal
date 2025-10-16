from datetime import date

from domain.model import UserRegister, UserLogin
from domain.interfaces.user_repo import UserRepositoryInterface
from domain.interfaces.password_service import PasswordServiceInterface
from domain.interfaces.jwt_service import JWTServiceInterface
from domain.exceptions import BadRequestError, NotFoundError
import re

def validate_phone_number(phone):
    """
    Validates Safari (Safaricom) and Ethio Telecom phone numbers.
    Returns 'safari', 'ethio', or 'invalid'.
    """

    # Normalize input (remove spaces, dashes, etc.)
    phone = phone.replace(" ", "").replace("-", "")

    # Ethio Telecom patterns (Ethiopia): 09xxxxxxxx or +2519xxxxxxxx
    ethio_pattern = re.compile(r"^(?:\+2519|09)\d{8}$")

    # Safaricom patterns (Kenya): 07xxxxxxxx, 01xxxxxxxx or +2547/1xxxxxxxx
    safari_pattern = re.compile(r"^(?:\+2547|\+2541|07|01)\d{8}$")

    if ethio_pattern.match(phone):
        return True
    elif safari_pattern.match(phone):
        return True
    else:
        return False

   
class UserUseCase:
    def __init__(self, user_repo: UserRepositoryInterface, pass_service: PasswordServiceInterface, jwt_service: JWTServiceInterface):
        self.jwt_service = jwt_service 
        self.user_repo = user_repo
        self.pass_service = pass_service

    def _ethiopian_year(self) -> int:
        g = date.today()
        if (g.month > 9) or (g.month == 9 and g.day >= 11):
            return g.year - 7
        return g.year - 8

    async def register_user(self, user: UserRegister):
        MIN_ID = 123456
        STEP = 125

        eth_year = self._ethiopian_year()
        year_suffix = f"{eth_year % 100:02d}"
        # check if phone number already exists
        if not validate_phone_number(user.phone_number):
            raise BadRequestError("Invalid phone number")
        
        user.phone_number = user.phone_number.replace(" ", "").replace("-", "")
        user.phone_number = user.phone_number[-8:]

        existing_user = await self.user_repo.find_by_phone_number(user.phone_number)
        if existing_user:
            raise BadRequestError("Phone number already registered")

        # get max numeric prefix for this year, then add STEP (or start from MIN_ID)
        max_num = await self.user_repo.get_max_numeric_for_year(year_suffix)
        if max_num is None:
            numeric = MIN_ID
        else:
            numeric = max_num + STEP

        # assign person_id and try to create; retry if conflict (limited)
        
        person_id = f"{numeric}/{year_suffix}"
        user.person_id = person_id

        # hash password
        user.password = self.pass_service.hash_password(user.password)

        created = await self.user_repo.create(user)
        if not created:
            raise Exception("Failed to create user, please try again")  
        return {"message": "user created successfully", "person_id": person_id}

    async def  user_login(self, user_login: UserLogin):
        user= await self.user_repo.get_by_person_id(user_login.id)
        if not user:
            raise NotFoundError("User Not Found")
        if not self.pass_service.verify_password(user_login.password, user.hashed_password):
            raise BadRequestError("Invalid Password")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(user.roles)
        access_token = self.jwt_service.create_access_token(data={"sub": user.person_id, "roles": [role.type_id.value for role in user.roles]})
        refresh_token = self.jwt_service.create_refresh_token(data={"sub": user.person_id})

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
        

        

