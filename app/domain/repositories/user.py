from abc import ABC, abstractmethod
from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get(self, *, id: int|None = None, login: str|None = None) -> User | None:
        pass
    
    @abstractmethod
    async def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass