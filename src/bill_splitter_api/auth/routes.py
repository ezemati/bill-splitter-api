from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from ..dependencies import SessionDep
from ..models import User
from .schemas import LoginResponse, RegisterRequest, UserResponse
from .security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"description": "Login successful"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
    },
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> LoginResponse:
    user = authenticate_user(session, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return LoginResponse(
        access_token=create_access_token(
            data={"sub": str(user.id), "username": user.username, "email": user.email}
        ),
        refresh_token="fakerefreshtoken",
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        ),
    )


@router.post(
    "/register",
    responses={
        status.HTTP_201_CREATED: {"description": "User registered successfully"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Username or email already exists"
        },
    },
)
async def register(
    request: RegisterRequest,
    session: SessionDep,
) -> JSONResponse:
    existing_user = session.scalars(
        select(User).where(
            (User.username == request.username) | (User.email == request.email)
        )
    ).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    user = User(
        username=request.username,
        email=request.email,
        password_hash=get_password_hash(request.password),
    )
    session.add(user)
    session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User registered successfully"},
    )
