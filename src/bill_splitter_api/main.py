from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from alembic import command, config

from .admin import admin_router
from .auth import auth_router
from .bill import bill_router
from .core import BaseSchema, get_project_root_path, settings
from .dependencies import SessionDep
from .user import user_router

main_router = APIRouter()


@main_router.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


class HealthCheckResponse(BaseSchema):
    api: str
    db: str


@main_router.get("/health")
def health_check(session: SessionDep) -> HealthCheckResponse:
    _ = session.execute(text("SELECT 1"))
    return HealthCheckResponse(api="ok", db="ok")


@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_cfg = config.Config(get_project_root_path() / "alembic.ini")
    if settings.db.run_migrations_on_startup:
        command.upgrade(alembic_cfg, "head")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(bill_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
