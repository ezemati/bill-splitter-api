from uuid import UUID

from pydantic import BaseModel


class MeResponse(BaseModel):
    id: UUID
    username: str
    email: str
