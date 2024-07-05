from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field

class BaseUserProject(BaseModel):
    project_id: UUID
    investment_sum: Decimal = Field(gt=0)

class UserProjectDB(BaseUserProject):
    user_id: UUID
    join_datetime: datetime

    class Config: 
        orm_mode: True