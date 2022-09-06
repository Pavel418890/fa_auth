from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api.deps import get_current_active_user, get_current_user, get_db
from app.core import security

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def create_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
        )
    else:
        return {
            "access_token": security.create_access_token(subject=user.id),
            "token_type": "bearer",
        }


@router.get("/login/test-token", response_model=schemas.User)
async def check_access_token(
    current_user: models.User = Depends(get_current_user),
) -> Optional[models.User]:
    return current_user
