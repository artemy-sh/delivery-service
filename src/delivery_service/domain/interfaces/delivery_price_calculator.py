from typing import Protocol

from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate
from delivery_service.domain.value_objects.money import Money


class IDeliveryPriceCalculator(Protocol):
    """
    Interface for calculating delivery price.
    """

    def calculate(
        self, parcel: Parcel, exchange_rate: ExchangeRate
    ) -> Money: ...
