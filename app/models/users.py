import uuid
import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class UserTypes(enum.Enum):
    user = 0 #(registered but not paid)
    super_admin = 1 #super administrator(all rights)
    superuser = 2 #registered and paid
    admin = 3 #administrator(restricted rights)

class StatusTypes(enum.Enum):
    inactive = 0
    active = 1
    deleted = 2

class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    status = Column(Integer, nullable=False, default=StatusTypes.active.value)
    type_id = Column(Integer, nullable=False, default=UserTypes.user.value)

    details = relationship("UsersDetails", uselist=False, back_populates="users")
    

class UsersDetails(Base):
    __tablename__ = "users_details"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)

    users = relationship("Users", back_populates="details")