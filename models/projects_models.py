from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.types import DateTime

from models.users_models import Base

import uuid

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    total_required_investmenet = Column(Integer, default=0)
    remaining_required_investment = Column(Integer, default=0)
    tags = Column(ARRAY(String))

    class Config:
        orm_mode = True