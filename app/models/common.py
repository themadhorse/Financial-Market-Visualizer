from pydantic import BaseModel


class Asset(BaseModel):
    symbol: str
    name: str
    quantity: int
    asset_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "name": "Apple Inc",
                "quantity": 5,
                "asset_type": "EQUITY",
            }
        }
