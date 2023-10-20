from fastapi import APIRouter, HTTPException
from firebase_admin import db
import json
from json import JSONDecodeError
from .common import call
from ..models.common import AssetDailyData, AssetQuote

userDbRef = db.reference().child("users")

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get(
    "",
    response_description="Information of assets passed",
    response_model=AssetDailyData,
)
async def get_asset_info(asset_symbol_str: str):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={asset_symbol_str}&interval=5min&outputsize=compact"

        result = AssetDailyData.parse_obj(json.loads(await call(url)))

    except JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON string passed")
    except Exception:
        raise HTTPException(status_code=500, detail="Fetching asset data failed")

    return result


@router.get(
    "/quote",
    response_description="Returns recent information about an asset",
    response_model=AssetQuote,
)
async def get_asset_quote(asset_symbol: str):
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={asset_symbol}"

        result = AssetQuote.parse_obj(json.loads(await call(url)))

    except JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON string passed")
    except Exception:
        raise HTTPException(status_code=500, detail="Fetching asset data failed")

    return result
