from sqlalchemy.orm import joinedload
from sqlalchemy.sql import select

from delivery_service.application.repositories.parcel_repository import (
    IParcelRepository,
)
from delivery_service.domain.entities.parcel import Parcel
from delivery_service.domain.entities.parcel_type import ParcelType
from delivery_service.domain.value_objects.enums import Currency
from delivery_service.domain.value_objects.money import Money
from delivery_service.domain.value_objects.parcel_id import ParcelId
from delivery_service.domain.value_objects.parcel_weight import ParcelWeight
from delivery_service.domain.value_objects.user_id import UserId
from delivery_service.infrastructure.sqlalchemy.models.parcel import (
    ParcelModel,
)
from delivery_service.infrastructure.sqlalchemy.repositories.repository import (
    SQLAlchemyRepository,
)


class ParcelRepository(
    SQLAlchemyRepository[Parcel, ParcelModel], IParcelRepository
):
    """
    SQLAlchemy repository for managing parcels.
    """

    _model_class: type[ParcelModel] = ParcelModel

    def _model_to_entity(
        self, model: ParcelModel, with_parcel_type_name: bool = False
    ) -> Parcel:
        """
        Maps ORM parcel model to domain entity.
        """
        return Parcel(
            id=ParcelId.from_str(model.id),
            name=model.name,
            weight=ParcelWeight(model.weight),
            parcel_type=ParcelType(
                id=model.parcel_type_id,
                name=model.parcel_type.name if with_parcel_type_name else None,
            ),
            user_id=UserId.from_str(model.user_id),
            price=Money(model.price, Currency(model.price_currency)),
            delivery_price=(
                Money(model.delivery_price, Currency(model.delivery_currency))
                if model.delivery_price is not None
                else None
            ),
        )

    def _entity_to_model(self, entity: Parcel) -> ParcelModel:
        """
        Maps domain parcel entity to ORM model.
        """
        return ParcelModel(
            id=str(entity.id),
            name=entity.name,
            weight=entity.weight.value,
            parcel_type_id=entity.parcel_type.id,
            user_id=str(entity.user_id),
            price=entity.price.value,
            price_currency=entity.price.currency.value,
            delivery_price=(
                entity.delivery_price.value if entity.delivery_price else None
            ),
            delivery_currency=(
                entity.delivery_price.currency.value
                if entity.delivery_price
                else None
            ),
        )

    async def get_by_id(self, id: str) -> Parcel | None:
        """
        Returns parcel by ID with joined parcel type.
        """
        query = (
            select(self._model_class)
            .options(joinedload(self._model_class.parcel_type))
            .filter_by(id=id)
        )
        result = await self._session.execute(query)
        model = result.scalars().one_or_none()

        return (
            self._model_to_entity(model, with_parcel_type_name=True)
            if model
            else None
        )

    async def find_all_by_filters(
        self,
        user_id: str,
        parcel_type_id: int | None = None,
        has_delivery_price: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Parcel]:
        """
        Returns filtered and paginated list of parcels for a user.
        """
        query = (
            select(self._model_class)
            .options(joinedload(self._model_class.parcel_type))
            .where(self._model_class.user_id == user_id)
        )

        if parcel_type_id:
            query = query.where(
                self._model_class.parcel_type_id == parcel_type_id
            )

        if has_delivery_price is True:
            query = query.where(self._model_class.delivery_price.is_not(None))
        elif has_delivery_price is False:
            query = query.where(self._model_class.delivery_price.is_(None))

        query = query.limit(limit).offset(offset)

        result = await self._session.execute(query)
        models = result.scalars().all()

        return [
            self._model_to_entity(model, with_parcel_type_name=True)
            for model in models
        ]
