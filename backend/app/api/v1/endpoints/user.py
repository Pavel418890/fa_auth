from ctypes import Union
from typing import Any, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post(
    "/", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
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
) -> list[models.User]:
    users = await crud.user.get_list(db=db, offset=offset, limit=limit)
    return users


@router.get("/me", response_model=schemas.User)
async def read_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    email: EmailStr = Body(None),
    password: str = Body(None),
    phone: str = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    current_user_data = jsonable_encoder(current_user)
    update_data = schemas.UserUpdate(**current_user_data)
    if email is not None:
        update_data.email = email
    if password is not None:
        update_data.password = password
    if phone is not None:
        update_data.phone = phone
    return await crud.user.update(
        db, user_in_db=current_user, data=update_data
    )


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(
    *,
    db: AsyncSession = Depends(deps.get_db),
    existing_user: models.User = Depends(deps.get_user_by_id)
) -> Any:
    return existing_user


@router.put("{user_id}", response_model=schemas.User)
async def update_user_by_id(
    *,
    db: AsyncSession = Depends(deps.get_db),
    new_user_data: schemas.UserUpdate,
    existing_user: models.User = Depends(deps.get_user_by_id)
) -> Any:
    return await crud.user.update(
        db, user_in_db=existing_user, data=new_user_data
    )
