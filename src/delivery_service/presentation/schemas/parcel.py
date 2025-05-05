from typing import Annotated, Optional

from pydantic import BaseModel, Field


class ParcelResponse(BaseModel):
    """
    Response schema for parcel with delivery price.
    """

    id: Annotated[str, Field(description="Parcel ID")]
    name: Annotated[str, Field(description="Parcel name")]
    weight: Annotated[float, Field(description="Weight in kg")]
    parcel_type: Annotated[
        str,
        Field(description="Parcel type"),
    ]
    price_usd: Annotated[float, Field(description="Price parcel in USD")]
    delivery_price_rub: Annotated[
        Optional[float],
        Field(
            description="Delivery price in RUB, or null if not calculated yet"
        ),
    ]
