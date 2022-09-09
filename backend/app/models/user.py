import typing
import uuid

from sqlalchemy import Boolean, CheckConstraint, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if typing.TYPE_CHECKING:
    from .profile import Profile  # noqa


class User(Base):
    __tablename__ = "app_user"
    __table_args__ = (
        CheckConstraint("email IS NOT NULL OR phone IS NOT NULL"),
    )
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    email = Column(String, index=True, unique=True)
    phone = Column(String, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True, server_default="true")
    is_superuser = Column(Boolean(), default=False, server_default="false")
    profile = relationship("Profile", back_populates="owner", uselist=False)
