from uuid import UUID

from pydantic import BaseModel


class IdTextPair(BaseModel):
    id: UUID
    text: str
