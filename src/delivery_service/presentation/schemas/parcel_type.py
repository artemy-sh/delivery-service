from typing import Annotated

from pydantic import BaseModel, Field


class ParcelTypeResponse(BaseModel):
    """
    Response schema for parcel type.
    """

    id: Annotated[int, Field(description="Parcel type ID")]
    name: Annotated[str, Field(description="Parcel type name")]

    model_config = {"from_attributes": True}
