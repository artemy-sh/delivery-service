from unittest.mock import AsyncMock

import pytest

from delivery_service.application.interfaces.cache import ICache
from delivery_service.application.interfaces.exchange_rate import IExchangeRate
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.entities.parcel_type import ParcelType
from delivery_service.domain.interfaces.delivery_price_calculator import (
    IDeliveryPriceCalculator,
)
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.parcel_id import ParcelId
from delivery_service.domain.value_objects.parcel_weight import ParcelWeight
from delivery_service.domain.value_objects.user_id import UserId


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def fake_logger() -> AsyncMock:
    return AsyncMock(spec=ILogger)


@pytest.fixture
def fake_rate_provider() -> AsyncMock:
    return AsyncMock(spec=IExchangeRate)


@pytest.fixture
def fake_price_calculator() -> AsyncMock:
    return AsyncMock(spec=IDeliveryPriceCalculator)


@pytest.fixture
def fake_redis_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def fake_cache() -> AsyncMock:
    mock = AsyncMock(spec=ICache)
    mock.get.return_value = 100.0
    return mock


@pytest.fixture
def parcel_type() -> ParcelType:
    return ParcelType(id=1, name="TestParcelType")


@pytest.fixture
def parcel(parcel_type: ParcelType) -> Parcel:
    return Parcel(
        id=ParcelId.new(),
        user_id=UserId.new(),
        name="TestParcel",
        parcel_type=parcel_type,
        weight=ParcelWeight(5.5),
        price=Money(15, Currency.USD),
    )
