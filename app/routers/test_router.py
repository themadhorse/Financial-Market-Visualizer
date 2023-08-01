from fastapi import APIRouter

router = APIRouter(prefix="/test")

@router.get("")
def send_msg():
    return "Routing works"

