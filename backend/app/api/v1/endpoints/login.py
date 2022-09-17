from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api.deps import get_current_user, get_db
from app.core import security
from app.core.config import settings

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


@router.get("/oauth2github")
async def login_oauth(request: Request):
    state = request.session
    return RedirectResponse(
        "https://github.com/login/oauth/authorize?"
        f"client_id={settings.GITHUB_CLIENT_ID}&"
        f"redirect_uri={'http://localhost:8000/api/v1/auth/github-login'}"
    )


@router.get("/oauth2google")
async def oauth_google():
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"scope=https%3A//www.googleapis.com/auth/userinfo.email.read-only&"
        f"access_type=offline&"
        f"include_granted_scopes=true&"
        f"response_type=code&"
        f"redirect_uri=http%3A//localhost:8000/api/v1/auth/google-login&"
        f"client_id={settings.GOOGLE_CLIENT_ID}"
    )


@router.get("/github-login")
async def authorize(request: Request):
    async with AsyncClient() as session:
        response = await session.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_SECRET_KEY,
                "code": request.query_params["code"],
            },
        )
        result = response.text
        token = result.split("&")
        access_token = token[0].split("=")[1]
        res = await session.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        r = res.text
        return r


@router.get("/google-login")
async def authorize_google(request: Request):
    async with AsyncClient() as session:
        response = await session.post("https://")
