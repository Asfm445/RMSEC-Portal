from fastapi import APIRouter, Depends
from api.schema.user_schema import UserRegisterSchema, UserLogin
from api.dependencies import get_usecase
from api.dto.user_dto import from_user_register_schema_to_model, from_user_login_schema_to_model
from api.utilities.handle_errors import handle_service_result
router = APIRouter()





@router.post("/register")
@handle_service_result
async def user_register(user: UserRegisterSchema, usecase=Depends(get_usecase)):
    user=from_user_register_schema_to_model(user)
    return await usecase.register_user(user)

@router.post("/login")
@handle_service_result
async def user_login(user: UserLogin, usecase=Depends(get_usecase)):
    user=from_user_login_schema_to_model(user)
    return await usecase.user_login(user)