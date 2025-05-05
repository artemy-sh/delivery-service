from dataclasses import dataclass

from delivery_service.domain.entities.parcel_type import ParcelType
from delivery_service.domain.exceptions import DeliveryPriceAlreadySet
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.parcel_id import ParcelId
from delivery_service.domain.value_objects.parcel_weight import ParcelWeight
from delivery_service.domain.value_objects.user_id import UserId


@dataclass
class Parcel:
    """
    Parcel entity.
    """

    id: ParcelId
    user_id: UserId
    name: str
    parcel_type: ParcelType
    weight: ParcelWeight
    price: Money
    delivery_price: Money | None = None

    def set_delivery_price(self, price: Money) -> None:
        """
        Set delivery price.
        """
        if self.delivery_price is not None:
            raise DeliveryPriceAlreadySet("Delivery price already set")
        self.delivery_price = price
