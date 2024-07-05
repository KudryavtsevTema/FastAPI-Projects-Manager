from uuid import uuid4

from sqlalchemy import DECIMAL, Column, UUID, ForeignKey, DateTime, Float

from app.models.base import Base


class UserProjects(Base):
    __tablename__ = "user_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    join_datetime = Column(DateTime, nullable=False)
    investment_sum = Column(DECIMAL(10, 2), nullable=False)
