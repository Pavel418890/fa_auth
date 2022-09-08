from typing import Any, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, db: AsyncSession, *, id: Union[int, UUID4]
    ) -> Optional[ModelType]:
        return await db.get(self.model, ident=id)

    async def get_list(
        self, db: AsyncSession, *, offset: int = 0, limit: int = 100
    ) -> list[ModelType]:
        query = await db.execute(
            select(self.model).offset(offset).limit(limit)
        )
        result = query.scalars().all()
        return result

    async def create(
        self, db: AsyncSession, *, data: CreateSchemaType
    ) -> ModelType:
        received_data = jsonable_encoder(data)
        db_obj = self.model(**received_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        data: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        current_obj = jsonable_encoder(db_obj)
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)
        for field in current_obj:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(
        self, db: AsyncSession, *, id: Union[int, UUID4]
    ) -> ModelType:
        db_obj = db.query(self.model).get(id)
        await db.delete(db_obj)
        await db.commit()
        return db_obj
