import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from delivery_service.infrastructure.sqlalchemy.database import Base

if TYPE_CHECKING:
    from delivery_service.infrastructure.sqlalchemy.models.parcel_type import (
        ParcelTypeModel,
    )


class ParcelModel(Base):
    """
    SQLAlchemy model for parcels table.
    """

    __tablename__ = "parcels"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)

    user_id: Mapped[str] = mapped_column(
        String(36), nullable=False, index=True
    )

    parcel_type_id: Mapped[int] = mapped_column(
        ForeignKey("parcel_types.id"), nullable=False
    )
    parcel_type: Mapped["ParcelTypeModel"] = relationship(
        back_populates="parcels"
    )

    weight: Mapped[float] = mapped_column(Float, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    price_currency: Mapped[str] = mapped_column(
        String(length=3), nullable=False
    )

    delivery_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    delivery_currency: Mapped[str | None] = mapped_column(
        String(length=3), nullable=True
    )
