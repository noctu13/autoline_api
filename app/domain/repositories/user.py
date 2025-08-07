from abc import ABC, abstractmethod
from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def find_by_login(self, login: str) -> User | None:
        pass
    
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: int) -> User | None:
        pass