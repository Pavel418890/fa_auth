from typing import Any, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel
from sqlalchemy.orm import Session

from ..db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, db: Session, *, id: Union[int, UUID4]
    ) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    async def get_list(
        self, db: Session, *, offset: int = 0, limit: int = 100
    ) -> list[ModelType]:
        return db.query(self.model).offset(offset).limit(limit).all()

    async def create(
        self, db: Session, *, data: CreateSchemaType
    ) -> ModelType:
        received_data = jsonable_encoder(data)
        db_obj = self.model(**received_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
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
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def remove(self, db: Session, *, id: Union[int, UUID4]) -> ModelType:
        db_obj = db.query(self.model).get(id)
        db.delete(db_obj)
        db.commit()
        return db_obj
