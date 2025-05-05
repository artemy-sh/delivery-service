import pytest

from delivery_service.domain.exceptions import InvalidMoney
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money


def test_money_create() -> None:
    moneyUSD = Money(10, Currency("USD"))
    assert moneyUSD.value == 10
    assert moneyUSD.currency is Currency.USD


def test_money_negative_value() -> None:
    with pytest.raises(InvalidMoney) as exc_info:
        Money(value=-10, currency=Currency.USD)
    assert "Money value cannot be negative" in str(exc_info.value)
