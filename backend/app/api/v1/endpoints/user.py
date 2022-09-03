from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_data: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    pass
