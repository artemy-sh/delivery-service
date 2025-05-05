from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from delivery_service.infrastructure.sqlalchemy.database import Base

if TYPE_CHECKING:
    from delivery_service.infrastructure.sqlalchemy.models.parcel import (
        ParcelModel,
    )


class ParcelTypeModel(Base):
    """
    SQLAlchemy model for parcel types table.
    """

    __tablename__ = "parcel_types"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)

    parcels: Mapped[list["ParcelModel"]] = relationship(
        back_populates="parcel_type"
    )
