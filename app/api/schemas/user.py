from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    login: str
    password: str


class UserCreateSchema(BaseModel):
    login: str
    password: str
    full_name: str
    role_id: int