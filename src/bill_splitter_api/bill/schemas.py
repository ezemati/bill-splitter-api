from datetime import datetime
from uuid import UUID

from pydantic import Field, field_validator

from ..core import BaseSchema


class ParticipantSchema(BaseSchema):
    id: UUID
    name: str


class CreateBillItemRequest(BaseSchema):
    name: str = Field(min_length=1)
    amount: float = Field(gt=0)
    participants: list[UUID] = Field(min_length=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be empty")
        return value

    @field_validator("participants")
    @classmethod
    def validate_participants(cls, value: list[UUID]) -> list[UUID]:
        if len(value) != len(set(value)):
            raise ValueError("participants must be unique within a bill item")
        return value


class BillItemSchema(CreateBillItemRequest):
    id: UUID


class CreateBillRequest(BaseSchema):
    name: str = Field(min_length=1)
    participants: list[ParticipantSchema] = Field(min_length=1)
    bill_items: list[CreateBillItemRequest] = Field(min_length=1)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be empty")
        return value


class CreateBillResponse(BaseSchema):
    id: UUID
    name: str
    participants: list[ParticipantSchema]
    bill_items: list[BillItemSchema]
    created_at: datetime
