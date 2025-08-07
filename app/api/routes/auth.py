from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_auth_service, get_current_admin
from app.api.schemas.user import UserAuthSchema, UserCreateSchema
from app.domain.entities.user import User, UserCreateDTO
from app.domain.services.auth_service import AuthService


router = APIRouter(
    prefix='/auth',
    tags=['Пользователи']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateSchema, 
    auth_service: AuthService = Depends(get_auth_service),
    current_user: User = Depends(get_current_admin),
):
    user_dto = UserCreateDTO(
        login=user_data.login,
        password=user_data.password,
        full_name=user_data.full_name,
        role_id=user_data.role_id
    )
    user = await auth_service.create_user(user_dto)
    return {"message": "User created"}

@router.post('/login')
async def login_user(
    response: Response,
    user_data: UserAuthSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(
        login=user_data.login,
        password=user_data.password
    )
    access_token = auth_service.create_access_token(user)
    response.set_cookie('access_token', access_token, httponly=True)
    return {"message": "Logged in"}

@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('access_token')
    return {"message": "Logged out"}