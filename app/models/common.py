from pydantic import BaseModel
from typing import Dict, Any


class Metadata(BaseModel):
    information: str
    symbol: str
    last_refreshed: str
    output_size: str
    timezone: str

    class Config:
        json_schema_extra = {
            "example": {
                "information": "Daily Prices (open, high, low, close) and Volumes",
                "symbol": "aapl",
                "last_refreshed": "2023-10-19",
                "output_size": "Compact",
                "timezone": "US/Eastern",
            }
        }


class TimeSeries(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int

    class Config:
        json_schema_extra = {
            "example": {
                "open": 176.0000,
                "high": 177.8400,
                "low": 175.1900,
                "close": 175.8400,
                "volume": 59302863,
            }
        }


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


class AssetDailyData(BaseModel):
    metadata: Metadata
    time_series: Dict[str, TimeSeries]

    def parse_obj(data: Dict[str, Any]):
        data_metadata = data["Meta Data"]
        data_timeseries = data["Time Series (Daily)"]
        parsed_timeseries: Dict[str, TimeSeries] = {}
        for date in data_timeseries:
            parsed_timeseries[date] = TimeSeries(
                open=data_timeseries[date]["1. open"],
                high=data_timeseries[date]["2. high"],
                low=data_timeseries[date]["3. low"],
                close=data_timeseries[date]["4. close"],
                volume=data_timeseries[date]["5. volume"],
            )

        return AssetDailyData(
            metadata=Metadata(
                information=data_metadata["1. Information"],
                symbol=data_metadata["2. Symbol"],
                last_refreshed=data_metadata["3. Last Refreshed"],
                output_size=data_metadata["4. Output Size"],
                timezone=data_metadata["5. Time Zone"],
            ),
            time_series=parsed_timeseries,
        )

    class Config:
        json_schema_extra = {
            "example": {
                "metadata": {
                    "information": "Daily Prices (open, high, low, close) and Volumes",
                    "symbol": "aapl",
                    "last_refreshed": "2023-10-19",
                    "output_size": "Compact",
                    "timezone": "US/Eastern",
                },
                "time_series": {
                    "open": 176.0000,
                    "high": 177.8400,
                    "low": 175.1900,
                    "close": 175.8400,
                    "volume": 59302863,
                },
            }
        }


class AssetQuote(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    price: float
    volume: int
    latest_trading_day: str
    previous_close: float
    change: float
    change_percent: float

    def parse_obj(obj: Dict[str, Any]):
        data = obj["Global Quote"]
        return AssetQuote(
            symbol=data["01. symbol"],
            open=data["02. open"],
            high=data["03. high"],
            low=data["04. low"],
            price=data["05. price"],
            volume=data["06. volume"],
            latest_trading_day=data["07. latest trading day"],
            previous_close=data["08. previous close"],
            change=data["09. change"],
            change_percent=float(data["10. change percent"].split("%")[0]),
        )

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "IBM",
                "open": "138.6400",
                "high": "139.4050",
                "low": "137.9300",
                "price": "138.0100",
                "volume": "5314159",
                "latest_trading_day": "2023-10-19",
                "previous_close": "139.9700",
                "change": "-1.9600",
                "change_percent": "-1.4003%",
            }
        }
