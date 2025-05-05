import pytest

from delivery_service.application.interfaces.cache import ICache
from delivery_service.application.interfaces.logger import ILogger
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate
from delivery_service.infrastructure.services.cbr_exchange_rate import (
    CbrExchangeRate,
)


@pytest.mark.anyio
async def test_get_rate(fake_cache: ICache, fake_logger: ILogger) -> None:
    cbr_exchange_rate = CbrExchangeRate(fake_cache, fake_logger)
    exchange_rate: ExchangeRate = await cbr_exchange_rate.get_rate(
        Currency.USD, Currency.RUB
    )

    assert exchange_rate.from_currency is Currency.USD
    assert exchange_rate.to_currency is Currency.RUB
    assert exchange_rate.value > 0
    assert isinstance(exchange_rate.value, float)
