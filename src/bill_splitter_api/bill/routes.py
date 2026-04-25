from fastapi import APIRouter, status

from ..core import IdTextPair
from ..dependencies import CurrentUserDep, SessionDep
from .create_bill import (
    create_bill as _create_bill,
)
from .create_bill import (
    get_bill_items,
    get_participants,
)
from .schemas import (
    BillItemSchema,
    CreateBillRequest,
    CreateBillResponse,
)

router = APIRouter(prefix="/bills", tags=["bills"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bill(
    request: CreateBillRequest, session: SessionDep, current_user: CurrentUserDep
) -> CreateBillResponse:
    participants = get_participants(request)
    bill_items = get_bill_items(request, participants)
    bill = _create_bill(request, bill_items, current_user, session)
    return CreateBillResponse(
        id=bill.id,
        name=bill.name,
        bill_items=[
            BillItemSchema(
                id=bill_item.id,
                name=bill_item.name,
                amount=bill_item.amount,
                participants=[
                    IdTextPair(
                        id=bill_participant.participant.id,
                        text=bill_participant.participant.name,
                    )
                    for bill_participant in bill_item.bill_participants
                ],
            )
            for bill_item in bill.bill_items
        ],
        created_at=bill.created_at,
    )
