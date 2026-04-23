from fastapi import FastAPI
from pydantic import BaseModel

from .auth.routes import router as auth_router

app = FastAPI()
app.include_router(auth_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hi there!"}


class HealthCheckResponse(BaseModel):
    status: str
    message: str


@app.get("/health")
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok", message="API is healthy")
