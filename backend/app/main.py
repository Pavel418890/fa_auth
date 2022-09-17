from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(openapi_url=f"{settings.API_V1}/openapi.json")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(router=api_router, prefix=settings.API_V1)
