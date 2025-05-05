from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.exceptions import InvalidMoney
from delivery_service.domain.interfaces.delivery_price_calculator import (
    IDeliveryPriceCalculator,
)
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate
from delivery_service.domain.value_objects.money import Money


class DefaultPriceCalculator(IDeliveryPriceCalculator):
    def calculate(self, parcel: Parcel, exchange_rate: ExchangeRate) -> Money:
        """
        Default calculates delivery price.
        """
        if parcel.price.currency != exchange_rate.from_currency:
            raise InvalidMoney("Currency mismatch for exchange rate")

        return Money(
            value=(parcel.weight.value * 0.5 + parcel.price.value * 0.01)
            * exchange_rate.value,
            currency=exchange_rate.to_currency,
        )
