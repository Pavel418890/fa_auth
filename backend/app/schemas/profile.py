from typing import Optional

from pydantic import UUID4, BaseModel

__all__ = ["Profile", "ProfileCreate", "ProfileUpdate", "ProfileInDB"]


class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    telegram: Optional[str] = None
    bio: Optional[str] = None
    social_name: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    picture: str = "default.png"


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileInDBBase(ProfileBase):
    id: int
    owner_id: UUID4

    class Config:
        orm_mode = True


class Profile(ProfileInDBBase):
    pass


class ProfileInDB(ProfileInDBBase):
    pass
