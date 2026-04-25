from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..core import IdTextPair


class CreateBillItemRequest(BaseModel):
    name: str = Field(min_length=1)
    amount: float = Field(gt=0)
    participants: list[IdTextPair] = Field(min_length=1)


class BillItemSchema(CreateBillItemRequest):
    id: UUID


class CreateBillRequest(BaseModel):
    name: str = Field(min_length=1)
    bill_items: list[CreateBillItemRequest] = Field(min_length=1)


class CreateBillResponse(BaseModel):
    id: UUID
    name: str
    bill_items: list[BillItemSchema]
    created_at: datetime
