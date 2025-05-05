from delivery_service.application.exceptions import (
    ApplicationError,
    DatabaseException,
)
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.domain.entities.parcel import Parcel


class GetUserParcelsUseCase:
    """
    Use case for fetching parcels by user.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        repository: type[IParcelRepository],
        logger: ILogger,
    ):
        self._repository: type[IParcelRepository] = repository
        self._uow: IUnitOfWork = uow
        self._logger = logger

    async def __call__(
        self,
        user_id: str,
        parcel_type_id: int | None = None,
        has_delivery_price: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Parcel]:
        """
        Returns filtered and paginated list of user's parcels.
        """
        try:
            self._logger.info(
                f"Requested list of parcel types from user {user_id} with filters: "
                f"parcel_type_id={parcel_type_id}, has_delivery_price={has_delivery_price}, "
                f"limit={limit}, offset={offset}"
            )
            async with self._uow as uow:
                repository = self._repository(uow)
                result: list[Parcel] = await repository.find_all_by_filters(
                    user_id, parcel_type_id, has_delivery_price, limit, offset
                )
            return result
        except DatabaseException as e:
            self._logger.error(f"Failed to get user parcels: {e}")
            raise ApplicationError("Failed to get user parcels")
