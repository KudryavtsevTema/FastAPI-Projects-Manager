from uuid import UUID
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field

class UserProject(BaseModel):
    project_id: UUID
    investment_sum: Decimal = Field(gt=0)

class UserProjectDB(UserProject):
    user_id: UUID
    join_datetime: datetime

    class Config: 
        orm_mode: True