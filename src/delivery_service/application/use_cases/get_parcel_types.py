from delivery_service.application.exceptions import (
    ApplicationError,
    DatabaseException,
)
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_type_repository import (
    IParcelTypeRepository,
)
from delivery_service.domain.entities.parcel_type import ParcelType


class GetParcelTypesUseCase:
    """
    Use case for fetching all parcel types.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        repository: type[IParcelTypeRepository],
        logger: ILogger,
    ):
        self._repository: type[IParcelTypeRepository] = repository
        self._uow: IUnitOfWork = uow
        self._logger = logger

    async def __call__(self) -> list[ParcelType]:
        """
        Returns list of all parcel types from repository.
        """
        try:
            self._logger.info("Requested list of parcel types")
            async with self._uow as uow:
                repository = self._repository(uow)
                result: list[ParcelType] = await repository.find_all()
            return result
        except DatabaseException as e:
            self._logger.error(f"Failed to get parcel types: {e}")
            raise ApplicationError("Failed to get parcel types")
