from delivery_service.application.interfaces.cache import ICache
from delivery_service.application.interfaces.exchange_rate import IExchangeRate
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.application.use_cases.register_parcel import (
    RegisterParcelUseCase,
)
from delivery_service.domain.interfaces.delivery_price_calculator import (
    IDeliveryPriceCalculator,
)
from delivery_service.domain.services.default_price_calculator import (
    DefaultPriceCalculator,
)
from delivery_service.infrastructure.logger.factory import LoggerFactory
from delivery_service.infrastructure.rabbitmq.consumer import ParcelConsumer
from delivery_service.infrastructure.services.cbr_exchange_rate import (
    CbrExchangeRate,
)
from delivery_service.infrastructure.services.redis_cache import (
    RedisCache,
)
from delivery_service.infrastructure.sqlalchemy.repositories.parcel import (
    ParcelRepository,
)
from delivery_service.infrastructure.sqlalchemy.unit_of_work import (
    SQLAlchemyUnitOfWork,
)


def get_logger() -> ILogger:
    return LoggerFactory().get_logger()


def get_register_parcel_uc(logger: ILogger) -> RegisterParcelUseCase:
    """
    Builds RegisterParcelUseCase with all dependencies.
    """
    uow: IUnitOfWork = SQLAlchemyUnitOfWork()
    repository: type[IParcelRepository] = ParcelRepository
    cache_service: ICache = RedisCache(logger)
    rate_provider: IExchangeRate = CbrExchangeRate(cache_service, logger)
    price_calculator: IDeliveryPriceCalculator = DefaultPriceCalculator()

    return RegisterParcelUseCase(
        uow,
        repository,
        rate_provider,
        price_calculator,
        logger,
    )


async def start_consumer() -> None:
    """
    Starts RabbitMQ consumer for parcel registration.
    """
    logger = get_logger()
    consumer = ParcelConsumer(
        register_parcel_uc=get_register_parcel_uc(logger), logger=logger
    )
    await consumer.start()
