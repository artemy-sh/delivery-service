from dataclasses import dataclass


@dataclass
class ParcelType:
    """
    Parcel type entity.
    """

    id: int
    name: str | None = None
