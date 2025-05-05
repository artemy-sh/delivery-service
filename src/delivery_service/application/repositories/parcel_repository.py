from typing import Any, Protocol

from delivery_service.application.repositories.repository import IRepository
from delivery_service.domain.entities.parcel import Parcel


class IParcelRepository(IRepository[Parcel], Protocol):
    """
    Repository interface for parcels.
    """

    async def find_all_by_filters(self, **filter_by: Any) -> list[Parcel]:
        """
        Returns parcels matching given filters.
        """
        ...
