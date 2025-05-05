import pytest

from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.exceptions import InvalidMoney
from delivery_service.domain.services.default_price_calculator import (
    DefaultPriceCalculator,
)
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.exchange_rate import ExchangeRate
from delivery_service.domain.value_objects.money import Money


def test_default_price_calculator(parcel: Parcel) -> None:
    default_calculator = DefaultPriceCalculator()
    exchange_rate = ExchangeRate(
        value=85.5, from_currency=Currency.USD, to_currency=Currency.RUB
    )
    result: Money = default_calculator.calculate(parcel, exchange_rate)

    assert result.value == (5.5 * 0.5 + 15 * 0.01) * 85.5
    assert result.currency is Currency.RUB


def test_default_price_calculator_currency_mismatch(parcel: Parcel) -> None:
    calculator = DefaultPriceCalculator()
    wrong_exchange_rate = ExchangeRate(
        value=90.0, from_currency=Currency.RUB, to_currency=Currency.USD
    )

    with pytest.raises(InvalidMoney) as exc_info:
        calculator.calculate(parcel, wrong_exchange_rate)

    assert "Currency mismatch" in str(exc_info.value)
