from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, validator

__all__ = ["User", "UserUpdate", "UserCreate", "UserInDB"]


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str

    @validator("phone")
    def check_email_or_phone(cls, phone, values) -> str:
        if "email" not in values and not phone:
            raise ValueError(
                "Either email or phone is required",
            )
        return phone


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[UUID4] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
