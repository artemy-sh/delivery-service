from typing import Protocol

from delivery_service.application.repositories.repository import IRepository
from delivery_service.domain.entities.parcel_type import ParcelType


class IParcelTypeRepository(IRepository[ParcelType], Protocol):
    """
    Repository interface for parcel types.
    """

    ...
