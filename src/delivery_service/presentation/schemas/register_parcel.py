from typing import Annotated

from pydantic import BaseModel, Field


class RegisterParcel(BaseModel):
    """
    Schemas for parcel registration.
    """

    name: Annotated[
        str, Field(min_length=1, max_length=255, description="Parcel name")
    ]
    weight: Annotated[float, Field(gt=0, description="Wight parcel in kg")]
    parcel_type_id: Annotated[int, Field(gt=0, description="Parcel type ID")]
    price_usd: Annotated[float, Field(gt=0, description="Price parcel in USD")]


class RegisterParcelResponse(BaseModel):
    """
    Schemas parcel ID after successful registration.
    """

    parcel_id: str
