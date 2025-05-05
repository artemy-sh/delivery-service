import pytest

from delivery_service.application.interfaces.logger import ILogger
from delivery_service.application.interfaces.unit_of_work import IUnitOfWork
from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.application.use_cases.get_parcel import GetParcelUseCase
from delivery_service.domain.entities.parcel import Parcel


@pytest.mark.anyio
async def test_get_parcel(
    fake_uow: IUnitOfWork,
    fake_repo_parcel: IParcelRepository,
    fake_logger: ILogger,
) -> None:
    use_case = GetParcelUseCase(
        uow=fake_uow,
        repository=fake_repo_parcel,
        logger=fake_logger,
    )

    result = await use_case("1")

    assert isinstance(result, Parcel)
    assert result.name == "TestParcel"
