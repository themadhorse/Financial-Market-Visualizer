from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId


class Stock(BaseModel):
    symbol: str
    name: str
    quantity: int


class UserModel(BaseModel):
    id: str = Field(default=str(ObjectId()))
    name: str
    portfolio: List[Stock] = Field(
        default=[], description="List of stocks in user's portfolio"
    )

    class Config:
        str_strip_whitespace = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {"example": {"name": "Harsh Kulkarni"}}
