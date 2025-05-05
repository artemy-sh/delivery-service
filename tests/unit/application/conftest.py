from types import TracebackType

import pytest

from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.application.repositories.parcel_type_repository import (
    IParcelTypeRepository,
)
from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.entities.parcel_type import ParcelType
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.parcel_id import ParcelId
from delivery_service.domain.value_objects.parcel_weight import ParcelWeight
from delivery_service.domain.value_objects.user_id import UserId


class FakeParcelTypeRepository(IParcelTypeRepository):
    def __init__(self, uow: IUnitOfWork = None) -> None:
        self._data = [
            ParcelType(id=1, name="Clothing"),
            ParcelType(id=2, name="Electronics"),
            ParcelType(id=3, name="Other"),
        ]

    async def find_all(self) -> list[ParcelType]:
        return self._data


class FakeParcelRepository(IParcelRepository):
    def __init__(self, uow: IUnitOfWork = None) -> None:
        self._parcels: list[Parcel] = [
            Parcel(
                id=ParcelId.new(),
                user_id=UserId.new(),
                name="TestParcel",
                parcel_type=ParcelType(id=1, name="TestParcelType"),
                weight=ParcelWeight(5.5),
                price=Money(15, Currency.USD),
            )
        ]

    async def get_by_id(self, id: int) -> Parcel | None:
        return self._parcels[0]

    async def add(self, entity: Parcel) -> Parcel | None:
        return self._parcels[0]

    async def find_all_by_filters(
        self,
        user_id: str,
        parcel_type_id: int | None = None,
        has_delivery_price: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[ParcelType]:
        return self._parcels


class FakeUnitOfWork(IUnitOfWork):
    async def __aenter__(self) -> IUnitOfWork:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    def __init__(self) -> None:
        self.committed = False

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.committed = False


@pytest.fixture
def fake_repo_parcel_type() -> IParcelTypeRepository:
    return FakeParcelTypeRepository


@pytest.fixture
def fake_repo_parcel() -> IParcelRepository:
    return FakeParcelRepository


@pytest.fixture
def fake_uow() -> IUnitOfWork:
    return FakeUnitOfWork()
