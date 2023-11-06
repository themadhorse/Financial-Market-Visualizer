from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Any


security = HTTPBearer()


async def get_firebase_user(
    token: HTTPAuthorizationCredentials = Depends(security),
) -> Any:
    if not token:
        raise HTTPException(
            status_code=400, detail="TokenID must be provided with all requests"
        )

    try:
        claims = auth.verify_id_token(token.credentials)
        return claims
    except InvalidIdTokenError:
        raise HTTPException(status_code=498, detail="Invalid Token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
