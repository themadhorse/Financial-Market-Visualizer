from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId

from .common import Asset


class UserModel(BaseModel):
    uid: str = Field(default=str(ObjectId()))
    name: str
    portfolio: List[Asset] = Field(
        default=[], description="List of stocks in user's portfolio"
    )

    class Config:
        str_strip_whitespace = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Harsh Kulkarni",
                "portfolio": [
                    {
                        "symbol": "AAPL",
                        "name": "Apple Inc",
                        "quantity": 5,
                        "asset_type": "EQUITY",
                    }
                ],
            }
        }
