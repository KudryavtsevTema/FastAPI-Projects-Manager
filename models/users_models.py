import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    disabled = Column(Boolean, nullable=True)
    type_id = Column(Integer, ForeignKey("user_type.id"), default=1)
    user_type = relationship("UserType", back_populates="users")

class UserType(Base):
    __tablename__ = "user_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    users = relationship("User", back_populates="user_type")