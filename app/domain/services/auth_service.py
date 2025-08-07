from app.core.exceptions import (RoleNotExistsException, 
    UserAlreadyExistsException, UserNotExistsException, WrongCredentialsException)
from app.domain.constants import RoleID
from app.domain.entities.user import User, UserCreateDTO
from app.domain.repositories.user import UserRepository
from app.domain.services.password_hasher import PasswordHasher
from app.domain.services.token_service import TokenService


class AuthService:
    def __init__(
            self, 
            user_repository: UserRepository, 
            password_hasher: PasswordHasher, 
            token_service: TokenService
    ):
        self.user_repo = user_repository
        self.password_hasher = password_hasher
        self.token_service = token_service
    
    async def create_user(self, user_dto: UserCreateDTO) -> User:
        existing_user = await self.user_repo.find_by_login(user_dto.login)
        if existing_user:
            raise UserAlreadyExistsException
        if user_dto.role_id not in RoleID.values_set():
            raise RoleNotExistsException
        hashed_password = self.password_hasher.hash(user_dto.password)
        user_dto.password = None
        user_entity = user_dto.to_user(hashed_password)
        return await self.user_repo.create_user(user_entity)
    
    async def authenticate_user(self, login: str, password: str) -> User:
        user = await self.user_repo.find_by_login(login)
        if (not user or 
            not self.password_hasher.verify(password, user.hashed_password)
        ):
            raise WrongCredentialsException
        return user
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotExistsException
        return user
    
    def create_access_token(self, user: User) -> str:
        return self.token_service.create_token({
            'sub': str(user.id),
            'type': 'access'
        })