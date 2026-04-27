from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str


class LoginResponse(BaseModel):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str
    user: UserResponse


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str


class JWTFields(BaseModel):
    sub: str
    username: str
    email: str
    exp: datetime
    admin: bool
