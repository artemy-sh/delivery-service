from uuid import uuid4

from fastapi import APIRouter, Depends, Query, Response

from delivery_service.application.dto.parcel import ParcelDTO
from delivery_service.application.use_cases.get_parcel import GetParcelUseCase
from delivery_service.application.use_cases.get_parcel_types import (
    GetParcelTypesUseCase,
)
from delivery_service.application.use_cases.get_user_parcels import (
    GetUserParcelsUseCase,
)
from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.entities.parcel_type import ParcelType
from delivery_service.infrastructure.rabbitmq.producer import ParcelProducer
from delivery_service.presentation.dependencies.parcel import (
    get_parcel_producer,
    get_parcel_types_uc,
    get_parcel_uc,
    get_user_parcels_uc,
)
from delivery_service.presentation.dependencies.user import (
    get_user_id_from_cookie,
)
from delivery_service.presentation.mappers.parcel import (
    map_entity_to_response,
    map_register_to_dto,
)
from delivery_service.presentation.schemas.parcel import ParcelResponse
from delivery_service.presentation.schemas.parcel_type import (
    ParcelTypeResponse,
)
from delivery_service.presentation.schemas.register_parcel import (
    RegisterParcel,
    RegisterParcelResponse,
)

router = APIRouter(prefix="/parcels", tags=["Parcels"])


@router.post("/")
async def register_parcel(
    parcel_dto: RegisterParcel,
    response: Response,
    user_id: str | None = Depends(get_user_id_from_cookie),
    parcel_producer: ParcelProducer = Depends(get_parcel_producer),
) -> RegisterParcelResponse:
    """
    Registers a new parcel with RabbitMQ and sets user cookie.
    """
    if not user_id:
        user_id = str(uuid4())
        response.set_cookie(
            key="user_id",
            value=user_id,
            httponly=True,
            samesite="lax",
            max_age=86400 * 30,
        )

    parcel_dto: ParcelDTO = map_register_to_dto(parcel_dto, user_id)
    await parcel_producer.publish(parcel_dto)
    return RegisterParcelResponse(parcel_id=parcel_dto.parcel_id)


@router.get("/{parcel_id}")
async def get_parcel_info(
    parcel_id: str,
    get_parcel_uc: GetParcelUseCase = Depends(get_parcel_uc),
) -> ParcelResponse:
    """
    Returns parcel details by ID.
    """
    parcel: Parcel = await get_parcel_uc(parcel_id)
    return map_entity_to_response(parcel)


@router.get("/")
async def get_user_parcels(
    parcel_type_id: int | None = Query(None),
    has_delivery_price: bool | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: str | None = Depends(get_user_id_from_cookie),
    get_user_parcel_uc: GetUserParcelsUseCase = Depends(get_user_parcels_uc),
) -> list[ParcelResponse] | None:
    """
    Returns user's parcels with optional filters and pagination.
    """
    if not user_id:
        return None

    parcels: list[Parcel] = await get_user_parcel_uc(
        user_id,
        parcel_type_id,
        has_delivery_price,
        limit,
        offset,
    )
    return [map_entity_to_response(p) for p in parcels]


@router.get("/types/")
async def get_parcel_types(
    get_parcel_types_uc: GetParcelTypesUseCase = Depends(get_parcel_types_uc),
) -> list[ParcelTypeResponse]:
    """
    Returns parcel types.
    """
    result: list[ParcelType] = await get_parcel_types_uc()
    return [ParcelTypeResponse.model_validate(p) for p in result]
