from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.infrastructure.database.models.role import RoleModel
from app.infrastructure.database.base import Base

class UserModel(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    
    role: Mapped[RoleModel] = relationship(back_populates="users")