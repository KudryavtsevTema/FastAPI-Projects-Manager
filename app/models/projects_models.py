import uuid

from sqlalchemy import Column, String, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.types import DateTime

from app.models.base import Base



class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    total_required_investmenet = Column(DECIMAL(10, 2), nullable=False)
    remaining_required_investment = Column(DECIMAL(10, 2))
    min_investment = Column(DECIMAL(10, 2), nullable=False)
    tags = Column(ARRAY(String))