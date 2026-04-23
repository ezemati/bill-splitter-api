from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .schemas import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"description": "Login successful"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
    },
)
async def login(request: LoginRequest) -> LoginResponse:
    if request.username != "testuser" or request.password != "testpassword":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return LoginResponse(
        access_token="fakeaccesstoken",
        refresh_token="fakerefreshtoken",
        user=UserResponse(id=1, username=request.username, email="fake@email.com"),
    )


@router.post(
    "/register",
    responses={
        status.HTTP_201_CREATED: {"description": "User registered successfully"},
    },
)
async def register() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "User registered successfully"},
    )
