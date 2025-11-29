from fastapi import APIRouter, Depends
from api.schema.user_schema import UserRegisterSchema, UserLogin, Refresh, StudentApplicationSchema
from api.dependencies import get_usecase, get_current_user
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

@router.post("/refresh")
@handle_service_result
async def refresh_token(refresh_token: Refresh, usecase=Depends(get_usecase)):
    return await usecase.refresh_token(refresh_token.refresh_token)


@router.post("/apply_student")
@handle_service_result
async def apply_student(application: StudentApplicationSchema, usecase=Depends(get_usecase),current_user=Depends(get_current_user)):
    return await usecase.apply_student(current_user["sub"], application.grade)