from typing import Optional

from pydantic import UUID4, BaseModel


class ProfileBase(BaseModel):
    telegram: Optional[str] = None
    bio: Optional[str] = None
    social_name: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    picture: str = "default.png"


class ProfileCreate(ProfileBase):
    social_name: str


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
