import pytest

from delivery_service.domain.exceptions import InvalidExchangeRate
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate


def test_exchange_rate_negative_value() -> None:
    with pytest.raises(InvalidExchangeRate) as exc_info:
        ExchangeRate(
            value=-3, from_currency=Currency.USD, to_currency=Currency.RUB
        )
    assert "Exchange Rate value cannot be negative" in str(exc_info.value)


def test_exchange_rate_zero_value() -> None:
    with pytest.raises(InvalidExchangeRate) as exc_info:
        ExchangeRate(
            value=0, from_currency=Currency.USD, to_currency=Currency.RUB
        )
    assert "Exchange Rate value cannot be zero" in str(exc_info.value)
