from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import text

from alembic import command, config

from .admin import admin_router
from .auth import auth_router
from .bill import bill_router
from .core import get_project_root_path, settings
from .dependencies import SessionDep
from .user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_cfg = config.Config(get_project_root_path() / "alembic.ini")
    if settings.db.run_migrations_on_startup:
        command.upgrade(alembic_cfg, "head")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(bill_router)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


class HealthCheckResponse(BaseModel):
    api: str
    db: str


@app.get("/health")
def health_check(session: SessionDep) -> HealthCheckResponse:
    _ = session.execute(text("SELECT 1"))
    return HealthCheckResponse(api="ok", db="ok")


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
