from typing import cast

from fastapi import Depends

from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.application.repositories.parcel_type_repository import (
    IParcelTypeRepository,
)
from delivery_service.application.use_cases.get_parcel import GetParcelUseCase
from delivery_service.application.use_cases.get_parcel_types import (
    GetParcelTypesUseCase,
)
from delivery_service.application.use_cases.get_user_parcels import (
    GetUserParcelsUseCase,
)
from delivery_service.infrastructure.rabbitmq.producer import ParcelProducer
from delivery_service.infrastructure.sqlalchemy.repositories.parcel import (
    ParcelRepository,
)
from delivery_service.infrastructure.sqlalchemy.repositories.parcel_type import (
    ParcelTypeRepository,
)
from delivery_service.presentation.dependencies.base import (
    get_logger_from_app,
    get_uow,
)


def get_parcel_repo() -> type[IParcelRepository]:
    """
    Returns parcel repository class.
    """
    return cast(type[IParcelRepository], ParcelRepository)


def get_parcel_types_repo() -> type[IParcelTypeRepository]:
    """
    Returns parcel type repository class.
    """
    return cast(type[IParcelTypeRepository], ParcelTypeRepository)


def get_parcel_producer(
    logger: ILogger = Depends(get_logger_from_app),
) -> ParcelProducer:
    """
    Returns configured RabbitMQ producer.
    """
    return ParcelProducer(logger)


def get_parcel_uc(
    uow: IUnitOfWork = Depends(get_uow),
    repository: type[IParcelRepository] = Depends(get_parcel_repo),
    logger: ILogger = Depends(get_logger_from_app),
) -> GetParcelUseCase:
    """
    Provides GetParcelUseCase with dependencies.
    """
    return GetParcelUseCase(uow, repository, logger)


def get_user_parcels_uc(
    uow: IUnitOfWork = Depends(get_uow),
    repository: type[IParcelRepository] = Depends(get_parcel_repo),
    logger: ILogger = Depends(get_logger_from_app),
) -> GetUserParcelsUseCase:
    """
    Provides GetUserParcelsUseCase with dependencies.
    """
    return GetUserParcelsUseCase(uow, repository, logger)


def get_parcel_types_uc(
    uow: IUnitOfWork = Depends(get_uow),
    repository: type[IParcelTypeRepository] = Depends(get_parcel_types_repo),
    logger: ILogger = Depends(get_logger_from_app),
) -> GetParcelTypesUseCase:
    """
    Provides GetParcelTypesUseCase with dependencies.
    """
    return GetParcelTypesUseCase(uow, repository, logger)
