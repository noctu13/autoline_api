from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import DatabaseException
from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository
from app.infrastructure.database.models.user import UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            login=model.login,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            role_id=model.role_id
        )
    
    async def find_by_login(self, login: str) -> User | None:
        query = select(UserModel).where(UserModel.login == login)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()
        if user_model:
            return self._to_entity(user_model)
        return None
    
    async def find_by_id(self, user_id: int) -> User | None:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user_model = result.scalar_one_or_none()
        if user_model:
            return self._to_entity(user_model)
        return None
    
    async def create_user(self, user: User) -> User:
        try:
            stmt = (
                insert(UserModel)
                .values(
                    login=user.login, 
                    hashed_password=user.hashed_password,
                    full_name=user.full_name,
                    role_id=user.role_id,
                )
                .returning(UserModel)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            user_model = result.scalar_one()
        except SQLAlchemyError as e:
            await self.session.rollback()
            print(str(e.__dict__['orig']))
            raise DatabaseException
        return self._to_entity(user_model)