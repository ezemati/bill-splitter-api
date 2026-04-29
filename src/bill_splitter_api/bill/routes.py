from fastapi import APIRouter, status

from ..dependencies import CurrentUserDep, SessionDep
from ..models import Bill
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
    ParticipantSchema,
)

router = APIRouter(prefix="/bills", tags=["bills"])


def bill_to_response(bill: Bill) -> CreateBillResponse:
    participant_ids = set()
    participants: list[ParticipantSchema] = []
    for bill_item in bill.bill_items:
        for participant in bill_item.participants:
            if participant.id in participant_ids:
                continue
            participants.append(
                ParticipantSchema(id=participant.id, name=participant.name)
            )
            participant_ids.add(participant.id)

    return CreateBillResponse(
        id=bill.id,
        name=bill.name,
        participants=participants,
        bill_items=[
            BillItemSchema(
                id=bill_item.id,
                name=bill_item.name,
                amount=bill_item.amount,
                participants=[p.id for p in bill_item.participants],
            )
            for bill_item in bill.bill_items
        ],
        created_at=bill.created_at,
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bill(
    request: CreateBillRequest, session: SessionDep, current_user: CurrentUserDep
) -> CreateBillResponse:
    participants = get_participants(request)
    bill_items = get_bill_items(request, participants)
    bill = _create_bill(request, bill_items, current_user, session)
    return bill_to_response(bill)
