from uuid import UUID

import pytest

from delivery_service.application.interfaces.exchange_rate import IExchangeRate
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.application.use_cases.register_parcel import (
    RegisterParcelUseCase,
)
from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.interfaces.delivery_price_calculator import (
    IDeliveryPriceCalculator,
)
from delivery_service.domain.value_objects.parcel_id import ParcelId


@pytest.mark.anyio
async def test_register_parcel(
    fake_uow: IUnitOfWork,
    fake_repo_parcel: IParcelRepository,
    fake_logger: ILogger,
    fake_price_calculator: IDeliveryPriceCalculator,
    fake_rate_provider: IExchangeRate,
    parcel: Parcel,
) -> None:
    use_case = RegisterParcelUseCase(
        uow=fake_uow,
        repository=fake_repo_parcel,
        rate_provider=fake_rate_provider,
        price_calculator=fake_price_calculator,
        logger=fake_logger,
    )

    result = await use_case(parcel)

    assert isinstance(result, ParcelId)
    assert isinstance(result.value, UUID)
