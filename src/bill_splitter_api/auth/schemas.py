from datetime import datetime
from uuid import UUID

from ..core import BaseSchema


class LoginRequest(BaseSchema):
    username: str
    password: str


class RegisterRequest(BaseSchema):
    username: str
    password: str
    email: str


class LoginResponse(BaseSchema):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str
    user: UserResponse


class UserResponse(BaseSchema):
    id: UUID
    username: str
    email: str


class JWTFields(BaseSchema):
    sub: str
    username: str
    email: str
    exp: datetime
    admin: bool
