from fastapi import APIRouter, Depends
from api.schema.user_schema import UserRegisterSchema
from api.dependencies import get_usecase

router = APIRouter()


# @router.post("/", response_model=Task)
# @handle_service_result
# async def create_task(
#     task: TaskCreate,
#     service=Depends(get_task_service),
#     current_user=Depends(get_current_user),
# ):
#     task = task_dto.pydantic_to_domain_task_create(task)
#     result = await service.create_task(task, current_user)  # await async service
#     return result


@router.post("/register")
async def user_register(user: UserRegisterSchema, usecase=Depends(get_usecase)):
    
    return await usecase.register_user(user)