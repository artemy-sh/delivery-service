from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.parcel_id import ParcelId
from delivery_service.domain.value_objects.user_id import UserId


def test_parcel_creation(parcel: Parcel) -> None:
    assert isinstance(parcel.id, ParcelId)
    assert isinstance(parcel.user_id, UserId)
    assert parcel.name == "TestParcel"
    assert parcel.parcel_type.name == "TestParcelType"
    assert parcel.parcel_type.id == 1
    assert parcel.weight.value == 5.5
    assert parcel.price.value == 15
    assert parcel.price.currency == Currency.USD
    assert parcel.delivery_price is None


def test_parcel_with_delivery_price(parcel: Parcel) -> None:
    delivery_price = Money(1200, Currency.RUB)
    parcel.delivery_price = delivery_price

    assert parcel.delivery_price.value == 1200
    assert parcel.delivery_price.currency == Currency.RUB
