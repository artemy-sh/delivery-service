from delivery_service.application.exceptions import (
    ApplicationError,
    DatabaseException,
    ParcelNotFoundError,
)
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.domain.entities.parcel import Parcel


class GetParcelUseCase:
    """
    Use case for fetching a parcel by ID.
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

    async def __call__(self, parcel_id: int) -> Parcel:
        """
        Returns parcel by ID or raises error if not found.
        """
        try:
            self._logger.info(f"Requested info of parcel: {parcel_id}")
            async with self._uow as uow:
                repository = self._repository(uow)
                result = await repository.get_by_id(parcel_id)
        except DatabaseException as e:
            self._logger.error(f"Failed to get parcel: {e}")
            raise ApplicationError("Failed to get parcel")

        if result is None:
            raise ParcelNotFoundError(f"Parcel with id {parcel_id} not found")

        return result
