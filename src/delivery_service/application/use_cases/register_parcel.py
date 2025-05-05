from delivery_service.application.exceptions import (
    DatabaseException,
)
from delivery_service.application.interfaces.exchange_rate import IExchangeRate
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.interfaces.delivery_price_calculator import (
    IDeliveryPriceCalculator,
)
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.parcel_id import ParcelId


class RegisterParcelUseCase:
    """
    Use case for registering a parcel and calculating its delivery price.
    """

    def __init__(
        self,
        uow: IUnitOfWork,
        repository: type[IParcelRepository],
        rate_provider: IExchangeRate,
        price_calculator: IDeliveryPriceCalculator,
        logger: ILogger,
    ):
        self._repository: type[IParcelRepository] = repository
        self._uow: IUnitOfWork = uow
        self._rate_provider: IExchangeRate = rate_provider
        self._price_calculator: IDeliveryPriceCalculator = price_calculator
        self._logger = logger

    async def __call__(self, parcel: Parcel) -> ParcelId:
        """
        Calculates delivery price and saves parcel to the database.
        """
        try:
            self._logger.info(
                f"Calculating delivery price for parcel: {parcel.id}"
            )
            exchange_rate = await self._rate_provider.get_rate(
                Currency.USD, Currency.RUB
            )
            delivery_price = self._price_calculator.calculate(
                parcel, exchange_rate
            )
            parcel.set_delivery_price(delivery_price)
        except Exception as e:
            self._logger.error(
                f"Failed to calculate delivery price parcel: {e}"
            )

        try:
            async with self._uow as uow:
                repository = self._repository(uow)
                result = await repository.add(parcel)
                self._logger.info(
                    f"Parcel with ID {parcel.id} successfully registered."
                )
            return result.id
        except DatabaseException as e:
            self._logger.error(f"Failed to register parcel: {e}")
