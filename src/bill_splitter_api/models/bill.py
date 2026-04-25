from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ModelBase
from .user import User


class Participant(ModelBase):
    name: Mapped[str] = mapped_column(nullable=False)
    bill_participants: Mapped[list[BillParticipant]] = relationship(
        back_populates="participant"
    )


class BillParticipant(ModelBase):
    """Many-to-many association table between BillItem and Participant"""

    participant_id: Mapped[UUID] = mapped_column(
        ForeignKey("participant.id"), nullable=False, index=True
    )
    participant: Mapped[Participant] = relationship(back_populates="bill_participants")

    bill_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("bill_item.id"), nullable=False, index=True
    )
    bill_item: Mapped[BillItem] = relationship(back_populates="bill_participants")


class BillItem(ModelBase):
    name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)

    bill_participants: Mapped[list[BillParticipant]] = relationship(
        back_populates="bill_item"
    )

    bill_id: Mapped[UUID] = mapped_column(
        ForeignKey("bill.id"), nullable=False, index=True
    )
    bill: Mapped[Bill] = relationship(back_populates="bill_items")


class Bill(ModelBase):
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    bill_items: Mapped[list[BillItem]] = relationship(back_populates="bill")
    created_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("user.id"), nullable=False, index=True
    )
    created_by: Mapped[User] = relationship()
