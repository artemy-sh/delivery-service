from uuid import UUID

import pytest

from delivery_service.domain.exceptions import InvalidUserId
from delivery_service.domain.value_objects.user_id import UserId


def test_parcel_id_accepts_valid_uuid() -> None:
    uid = UUID("12345678-1234-5678-1234-567812345678")
    pid = UserId(uid)
    assert isinstance(pid.value, UUID)
    assert str(pid) == str(uid)


def test_parcel_id_new_generates_uuid() -> None:
    pid = UserId.new()
    assert isinstance(pid.value, UUID)


def test_parcel_id_from_str_parses_string() -> None:
    string_id = "12345678-1234-5678-1234-567812345678"
    pid = UserId.from_str(string_id)
    assert isinstance(pid.value, UUID)
    assert str(pid) == string_id


def test_parcel_id_raises_on_invalid_type() -> None:
    with pytest.raises(InvalidUserId) as exc_info:
        UserId("not-a-uuid")
    assert "Expected UUID" in str(exc_info.value)
