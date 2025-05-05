from delivery_service.application.repositories.parcel_type_repository import (
    IParcelTypeRepository,
)
from delivery_service.domain.entities.parcel_type import ParcelType
from delivery_service.infrastructure.sqlalchemy.models.parcel_type import (
    ParcelTypeModel,
)
from delivery_service.infrastructure.sqlalchemy.repositories.repository import (
    SQLAlchemyRepository,
)


class ParcelTypeRepository(
    SQLAlchemyRepository[ParcelType, ParcelTypeModel], IParcelTypeRepository
):
    """
    SQLAlchemy repository for parcel types.
    """

    _model_class: type[ParcelTypeModel] = ParcelTypeModel

    def _model_to_entity(self, model: ParcelTypeModel) -> ParcelType:
        """
        Maps ORM model to domain entity.
        """
        return ParcelType(
            id=model.id,
            name=model.name,
        )

    def _entity_to_model(self, entity: ParcelType) -> ParcelTypeModel:
        """
        Maps domain entity to ORM model.
        """
        return ParcelTypeModel(
            id=entity.id,
            name=entity.name,
        )
