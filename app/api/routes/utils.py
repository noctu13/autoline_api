from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.domain.constants import RoleID
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.session import engine, get_async_db


router = APIRouter(
    prefix='/utils',
    tags=['Инструменты разработчика']
)

@router.post('/clear-tables')
async def clear_tables():
    if not settings.DEBUG_MODE:
        raise HTTPException(403, "Отладка запрещена!")
    print("Tables in metadata:")
    for table in Base.metadata.sorted_tables:
        print(f"- {table.name}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Таблицы очищены!"}

@router.post('/initialize-roles')
async def initialize_roles(session: AsyncSession = Depends(get_async_db)):
    if not settings.DEBUG_MODE:
        raise HTTPException(403, "Отладка запрещена!")
    roles_list = [RoleModel(id=role.value, name=role.name) for role in RoleID]
    session.add_all(roles_list)
    await session.commit()
    return {"message": "Роли инициализированы!"}