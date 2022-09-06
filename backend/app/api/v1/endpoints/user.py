from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_data: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    existing_user = await crud.user.get_by_email(db=db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exist",
        )
    else:
        new_user = await crud.user.create(db, data=user_data)
        return new_user


@router.get("/", response_model=list[schemas.User])
async def list_users(
    *,
    db: AsyncSession = Depends(deps.get_db),
    offset: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Optional[list[schemas.User]]:
    users = await crud.user.get_list(db=db, offset=offset, limit=limit)
    return users
