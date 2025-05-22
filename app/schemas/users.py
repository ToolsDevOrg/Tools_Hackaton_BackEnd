import uuid

from pydantic import BaseModel, EmailStr

from app.models.enums import UserRoleEnum


class SUserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: str
    fio: str
    role: UserRoleEnum


class SUserCurrent(BaseModel):
    id: uuid.UUID
    email: str
    phone: str
    fio: str
    jk_name: str
    role: UserRoleEnum


class SUserLogin(BaseModel):
    email: EmailStr
    password: str


class SUserTokens(BaseModel):
    access_token: str
    refresh_token: uuid.UUID
