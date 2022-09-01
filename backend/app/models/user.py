import typing
import uuid

from sqlalchemy import Boolean, CheckConstraint, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db import Base

if typing.TYPE_CHECKING:
    from .profile import Profile


class User(Base):
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)
    full_name = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    profile = relationship("Profile", back_populates="owner")

    CheckConstraint("email IS NOT NULL OR phone IS NOT NULL")
