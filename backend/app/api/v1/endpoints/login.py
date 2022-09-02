from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
async def create_access_token()