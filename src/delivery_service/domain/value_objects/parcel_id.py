import uuid
from dataclasses import dataclass

from delivery_service.domain.exceptions import InvalidParcelId


@dataclass(frozen=True)
class ParcelId:
    """
    Unique identifier for a parcel.
    """

    value: uuid.UUID

    def __post_init__(self) -> None:
        """
        Validates that value is a UUID.
        """
        if not isinstance(self.value, uuid.UUID):
            raise InvalidParcelId(
                f"Expected UUID, got: {type(self.value).__name__}"
            )

    @staticmethod
    def new() -> "ParcelId":
        """
        Generates a new ParcelId.
        """
        return ParcelId(uuid.uuid4())

    @staticmethod
    def from_str(value: str) -> "ParcelId":
        """
        Creates ParcelId from string.
        """
        return ParcelId(uuid.UUID(value))

    def __str__(self) -> str:
        """
        Returns UUID as string.
        """
        return str(self.value)
