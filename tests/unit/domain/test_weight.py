import pytest

from delivery_service.domain.exceptions import InvalidWeight
from delivery_service.domain.value_objects.parcel_weight import ParcelWeight


def test_parcel_weight_negative_value() -> None:
    with pytest.raises(InvalidWeight) as exc_info:
        ParcelWeight(0)
    assert "Parcel Weight cannot be negative" in str(exc_info.value)
