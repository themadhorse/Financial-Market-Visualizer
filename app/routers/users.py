from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from firebase_admin import db
from firebase_admin.exceptions import FirebaseError
from bson import ObjectId
from typing import List

from app.dependencies import get_firebase_user

from ..models.user import UserModel
from ..models.common import Asset

userDbRef = db.reference().child("users")

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_description="Created User document", response_model=UserModel)
def create_user(user: UserModel):
    user.uid = str(ObjectId()) if user.uid is None else user.uid
    user_json = jsonable_encoder(user)
    try:
        userDbRef.child(user.uid).set(user_json)
    except FirebaseError:
        raise HTTPException(
            status_code=500, detail="Push failed, firebase communication error"
        )

    return user


@router.get(
    "",
    response_description="User document with relevant token id",
    response_model=UserModel,
)
def get_user(uid: str, current_user=Depends(get_firebase_user)):
    # if current_user["uid"] != uid:
    #     raise HTTPException(status_code=400, detail="You may only request data about the logged in user")

    try:
        user = userDbRef.child(uid).get()
        return UserModel(**user)
    except FirebaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve data, firebase communication error",
        )


@router.delete("", status_code=204, response_description="Successful deletion")
def delete_user(uid: str):
    try:
        userDbRef.child(uid).delete()
    except FirebaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user, firebase communication error",
        )


@router.patch(
    "/portfolio",
    response_description="List of updated stocks",
    response_model=List[Asset],
)
def add_assets_to_user(
    uid: str,
    stocks: List[Asset]
    #  current_user = Depends(get_firebase_user)
):
    # if current_user["uid"] != uid:
    #     raise HTTPException(status_code=400, detail="You may only update the portfolio of the logged in user")
    try:
        portfolio: List[Asset] = userDbRef.child(f"{uid}/portfolio").get()
        portfolio.extend(stocks)

        userDbRef.child(f"{uid}/portfolio").set(jsonable_encoder(portfolio))
    except FirebaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to add to portfolio, firebase communication error",
        )

    return portfolio


@router.delete(
    "/portfolio",
    response_description="List of updated stocks",
    response_model=List[Asset],
)
def remove_assets_from_user(
    uid: str,
    stocks: List[Asset]
    #  current_user = Depends(get_firebase_user)
):
    # if current_user["uid"] != uid:
    #     raise HTTPException(status_code=400, detail="You may only update the portfolio of the logged in user")
    try:
        portfolio: List[Asset] = [
            Asset(**stock) for stock in userDbRef.child(f"{uid}/portfolio").get()
        ]
        updated_portfolio = [
            stock
            for stock in portfolio
            if stock.symbol not in [stock.symbol for stock in stocks]
        ]

        userDbRef.child(f"{uid}/portfolio").set(jsonable_encoder(updated_portfolio))
    except FirebaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to add to portfolio, firebase communication error",
        )

    return updated_portfolio
