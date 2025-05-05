from dataclasses import dataclass

from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.entities.parcel_type import ParcelType
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.parcel_id import ParcelId
from delivery_service.domain.value_objects.parcel_weight import ParcelWeight
from delivery_service.domain.value_objects.user_id import UserId


@dataclass
class ParcelDTO:
    """
    DTO for parcel data transfer.
    """

    parcel_id: str
    user_id: str
    name: str
    weight: float
    parcel_type_id: int
    price_usd: float


def map_dto_to_entity(parcel_dto: ParcelDTO) -> Parcel:
    """
    Mapping ParcelDTO to Parcel entity.
    """
    return Parcel(
        id=ParcelId.from_str(parcel_dto.parcel_id),
        user_id=UserId.from_str(parcel_dto.user_id),
        name=parcel_dto.name,
        parcel_type=ParcelType(parcel_dto.parcel_type_id),
        weight=ParcelWeight(parcel_dto.weight),
        price=Money(parcel_dto.price_usd, Currency.USD),
    )
