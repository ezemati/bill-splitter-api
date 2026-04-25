from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from ..models import Bill, BillItem, BillParticipant, Participant, User
from .schemas import CreateBillRequest


def get_participants(request: CreateBillRequest) -> dict[UUID, Participant]:
    participants = {}
    for bill_item_request in request.bill_items:
        for participant_request in bill_item_request.participants:
            if participant_request.id not in participants:
                participant = Participant(
                    id=participant_request.id,
                    name=participant_request.text,
                )
                participants[participant_request.id] = participant
    return participants


def get_bill_items(
    request: CreateBillRequest, participants: dict[UUID, Participant]
) -> list[BillItem]:
    bill_items = []
    for bill_item_request in request.bill_items:
        bill_item = BillItem(
            name=bill_item_request.name,
            amount=bill_item_request.amount,
        )

        for participant_request in bill_item_request.participants:
            participant = participants[participant_request.id]
            bill_participant = BillParticipant(
                participant=participant,
                bill_item=bill_item,
            )
            bill_item.bill_participants.append(bill_participant)

        bill_items.append(bill_item)
    return bill_items


def create_bill(
    request: CreateBillRequest,
    bill_items: list[BillItem],
    current_user: User,
    session: Session,
) -> Bill:
    bill = Bill(
        name=request.name,
        created_at=datetime.now(timezone.utc),
        bill_items=bill_items,
        created_by=current_user,
    )
    session.add(bill)
    session.commit()
    session.refresh(bill)
    return bill
