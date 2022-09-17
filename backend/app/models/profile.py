import typing

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if typing.TYPE_CHECKING:
    from .user import User  # noqa


class Profile(Base):
    id = Column(Integer, primary_key=True, index=True)
    social_name = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    location = Column(String)
    company = Column(String)
    bio = Column(Text)
    picture = Column(String, default="default.png")
    owner_id = Column(UUID(as_uuid=True), ForeignKey("app_user.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="profile")
