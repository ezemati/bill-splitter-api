from uuid import UUID


from ..core import BaseSchema


class MeResponse(BaseSchema):
    id: UUID
    username: str
    email: str
