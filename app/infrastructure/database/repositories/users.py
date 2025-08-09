from sqlalchemy import select, insert, update, delete
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
    
    async def _execute(self, stmt, commit=True):
        try:
            result = await self.session.execute(stmt)
            if commit:
                await self.session.commit()
        except SQLAlchemyError as e:
            if commit:
                await self.session.rollback()
            print(str(e.__dict__['orig']))
            raise DatabaseException
        if result:
            user_model = result.scalar_one_or_none()
            return self._to_entity(user_model) if user_model else None
    
    async def get(self, *, id: int|None = None, login: str|None = None) -> User | None:
        """
        user get universal method
        - get(id=123)                 -> by id
        - get(login="username")       -> by login
        """
        if id is not None and login is not None:
            raise ValueError("Only one parameter (id or login) can be provided")
        query = select(UserModel)
        if id is not None:
            query = query.where(UserModel.id == id)
        elif login is not None:
            query = query.where(UserModel.login == login)
        else:
            raise ValueError("Must provide either 'id' or 'login'")
        return await self._execute(query, commit=False)
    
    async def create(self, user: User) -> User:
        query = (
            insert(UserModel)
            .values(
                login=user.login, 
                hashed_password=user.hashed_password,
                full_name=user.full_name,
                role_id=user.role_id,
            )
            .returning(UserModel)
        )
        return await self._execute(query)
    
    async def update(self, user: User) -> User:
        query = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                login=user.login, 
                hashed_password=user.hashed_password,
                full_name=user.full_name,
                role_id=user.role_id,
            )
            .returning(UserModel)
        )
        return await self._execute(query)
    
    async def delete(self, user: User) -> None:
        query = (
            delete(UserModel)
            .where(UserModel.id == user.id)
        )
        return await self._execute(query)