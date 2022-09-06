from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=True
)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
    expire_on_commit=False,
)
