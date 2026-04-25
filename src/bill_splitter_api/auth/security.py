from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core import settings
from ..models import User

password_hasher = PasswordHasher()


def verify_password(hashed_password: str, plain_password: str) -> bool:
    try:
        _ = password_hasher.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def get_password_hash(plain_password: str):
    return password_hasher.hash(plain_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expires_delta = expires_delta or timedelta(minutes=15)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, settings.jwt.secret_key, settings.jwt.algorithm)
    return encoded_jwt


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = session.scalars(select(User).where(User.username == username)).first()
    if user is None:
        return None
    if not verify_password(user.password_hash, password):
        return None
    return user
