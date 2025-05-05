import pytest

from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_type_repository import (
    IParcelTypeRepository,
)
from delivery_service.application.use_cases.get_parcel_types import (
    GetParcelTypesUseCase,
)
from delivery_service.domain.entities.parcel_type import ParcelType


@pytest.mark.anyio
async def test_get_parcel_types(
    fake_uow: IUnitOfWork,
    fake_repo_parcel_type: IParcelTypeRepository,
    fake_logger: ILogger,
) -> None:
    use_case = GetParcelTypesUseCase(
        uow=fake_uow,
        repository=fake_repo_parcel_type,
        logger=fake_logger,
    )

    result = await use_case()

    assert isinstance(result, list)
    assert all(isinstance(p, ParcelType) for p in result)
    assert len(result) == 3
