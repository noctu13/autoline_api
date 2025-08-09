from fastapi import Cookie, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import (TokenInvalidClaimsException, 
    TokenInvalidException, TokenMissingException)
from app.core.security.permissions import check_admin
from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository
from app.domain.services.password_hasher import PasswordHasher
from app.domain.services.auth_service import AuthService
from app.domain.services.token_service import TokenService
from app.infrastructure.database.session import get_async_db
from app.infrastructure.database.repositories.users import SQLAlchemyUserRepository
from app.infrastructure.security.jwt_token_service import JWTTokenService
from app.infrastructure.security.passlib_password_hasher import PasslibPasswordHasher


def get_user_repository(session: AsyncSession = Depends(get_async_db)) -> UserRepository:
    return SQLAlchemyUserRepository(session)

def get_password_hasher() -> PasswordHasher:
    return PasslibPasswordHasher()

def get_token_service() -> TokenService:
    return JWTTokenService()

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    token_service: TokenService = Depends(get_token_service)
) -> AuthService:
    return AuthService(
        user_repo,
        password_hasher, 
        token_service
    )

async def get_current_user(
    access_token: str = Cookie(None, alias="access_token"),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    try:
        if not access_token:
            raise TokenMissingException
        payload = auth_service.token_service.verify_token(
            access_token)
        if payload.get("type") != "access":
            raise TokenInvalidClaimsException
        user_id = int(payload.get('sub'))
        user = await auth_service.get_user(user_id)
    except Exception as e:
        if settings.DEBUG_MODE:
            raise e
        raise TokenInvalidException
    return user

async def get_current_admin(
    user: User = Depends(get_current_user)
) -> User:
    check_admin(user)
    return user