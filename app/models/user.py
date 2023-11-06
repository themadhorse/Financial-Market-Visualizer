from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

from .common import Asset


class UserModel(BaseModel):
    uid: str = Field(default=str(ObjectId()))
    email: str
    photoURL: Optional[str]
    emailVerified: bool
    displayName: Optional[str]
    portfolio: List[Asset] = Field(
        default=[], description="List of stocks in user's portfolio"
    )

    class Config:
        str_strip_whitespace = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "displayName": "Harsh Kulkarni",
                "email": "harsh@email.com",
                "photoURL": "someurl.com",
                "emailVerified": True,
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
