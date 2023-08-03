from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from firebase_admin import db
from bson import ObjectId

from ..models.user import UserModel

userDbRef = db.reference().child("users")

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_description="Created User document")
def create_user(user: UserModel):
    user.id = str(ObjectId())
    user_json = jsonable_encoder(user)
    try:
        userDbRef.push(user_json)
    except Exception:
        raise HTTPException(status_code=500, detail="Push to firebase failed")

    return user
