from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core import settings
from ..models import User
from .schemas import JWTFields

password_hasher = PasswordHasher()


def verify_password(hashed_password: str, plain_password: str) -> bool:
    try:
        _ = password_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def get_password_hash(plain_password: str):
    return password_hasher.hash(plain_password)


def create_access_token(user: User):
    exp_minutes = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    exp = datetime.now(timezone.utc) + exp_minutes
    data = JWTFields(
        sub=str(user.id),
        username=user.username,
        email=user.email,
        exp=exp,
        admin=user.is_admin,
    )
    return jwt.encode(
        data.model_dump(),
        settings.jwt.secret_key,
        settings.jwt.algorithm,
    )


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = session.scalars(select(User).where(User.username == username)).first()
    if user is None:
        return None
    if not verify_password(user.password_hash, password):
        return None
    return user
