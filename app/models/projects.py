import uuid
import enum

from sqlalchemy import Column, ForeignKey, String, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime

from app.models.base import Base


class StatusType(enum.Enum):
    inactive = 0
    active = 1
    deleted = 2

class Projects(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Integer, nullable=False, default=StatusType.inactive.value)
    
    details = relationship("ProjectsDetails", uselist=False, back_populates="projects")

class ProjectsDetails(Base):
    __tablename__ = "projects_details"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    total_required_investment = Column(DECIMAL(10, 2), nullable=False)
    remaining_required_investment = Column(DECIMAL(10, 2))
    min_investment = Column(DECIMAL(10, 2), nullable=False)
    tags = Column(ARRAY(String))

    projects = relationship("Projects", back_populates="details")

