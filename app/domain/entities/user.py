from dataclasses import dataclass
from app.domain.constants import RoleID

@dataclass
class User:
    id: int
    login: str
    hashed_password: str
    full_name: str
    role_id: int

    def is_admin(self) -> bool:
        return self.role_id == RoleID.ADMIN.value

@dataclass
class UserCreateDTO:
    login: str
    password: str  # temporary field
    full_name: str
    role_id: int

    def to_user(self, hashed_password: str) -> User:
        return User(
            id=None,
            login=self.login,
            hashed_password=hashed_password,
            full_name=self.full_name,
            role_id=self.role_id
        )