from delivery_service.application.dto.parcel import ParcelDTO
from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.value_objects.parcel_id import ParcelId
from delivery_service.presentation.schemas.parcel import ParcelResponse
from delivery_service.presentation.schemas.register_parcel import (
    RegisterParcel,
)


def map_register_to_dto(
    parcel_register: RegisterParcel, user_id: str
) -> Parcel:
    """
    Converts registration scheme to ParcelDTO.
    """
    return ParcelDTO(
        parcel_id=str(ParcelId.new()),
        user_id=user_id,
        name=parcel_register.name,
        weight=parcel_register.weight,
        parcel_type_id=parcel_register.parcel_type_id,
        price_usd=parcel_register.price_usd,
    )


def map_entity_to_response(entity: Parcel) -> ParcelDTO:
    """
    Converts Parcel entity to response schema.
    """
    return ParcelResponse(
        id=str(entity.id),
        name=entity.name,
        weight=entity.weight.value,
        parcel_type=entity.parcel_type.name,
        price_usd=round(entity.price.value, 2),
        delivery_price_rub=round(entity.delivery_price.value, 2)
        if entity.delivery_price
        else None,
    )
