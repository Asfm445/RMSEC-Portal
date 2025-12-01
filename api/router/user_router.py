from fastapi import APIRouter, Depends
from api.schema.user_schema import UserRegisterSchema, UserLogin, Refresh, StudentApplicationSchema
from api.dependencies import get_usecase, get_current_user
from api.dto.user_dto import from_user_register_schema_to_model, from_user_login_schema_to_model
from api.utilities.handle_errors import handle_service_result
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()





@router.post("/register")
@handle_service_result
async def user_register(user: UserRegisterSchema, usecase=Depends(get_usecase)):
    user=from_user_register_schema_to_model(user)
    return await usecase.register_user(user)

@router.post("/token")
@handle_service_result
async def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    usecase= Depends(get_usecase)
):
    """
    Login endpoint compatible with FastAPI OAuth2 docs.
    Use 'username' for person_id and 'password' for password.
    """
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(form_data.__dict__)
    user_login_model = from_user_login_schema_to_model({
        "id": form_data.username,  # map username to your person_id
        "password": form_data.password
    })
    return await usecase.user_login(user_login_model)

@router.post("/refresh")
@handle_service_result
async def refresh_token(refresh_token: Refresh, usecase=Depends(get_usecase)):
    return await usecase.refresh_token(refresh_token.refresh_token)


@router.post("/apply_student")
@handle_service_result
async def apply_student(application: StudentApplicationSchema, usecase=Depends(get_usecase),current_user=Depends(get_current_user)):
    print("+++++++++++++++++++++++++++++++++++hre i router++++++++++++++++")
    print(current_user)
    return await usecase.apply_student(int(current_user["sub"]), application.grade)