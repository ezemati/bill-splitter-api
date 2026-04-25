from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text

from .admin import admin_router
from .auth import auth_router
from .bill import bill_router
from .db import engine
from .dependencies import SessionDep
from .models import ModelBase
from .user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    ModelBase.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(bill_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hi there!"}


class HealthCheckResponse(BaseModel):
    api: str
    db: str


@app.get("/health")
def health_check(session: SessionDep) -> HealthCheckResponse:
    _ = session.execute(text("SELECT 1"))
    return HealthCheckResponse(api="ok", db="ok")
