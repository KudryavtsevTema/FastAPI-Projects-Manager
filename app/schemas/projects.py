from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class BaseProject(BaseModel):
    name: str = Field(title="Название проекта", examples=["ХаляваОнлайн"])
    description: str | None = None
    start_at: date
    end_at: date
    total_required_investment: Decimal
    remaining_required_investment: Decimal
    min_investment: Decimal
    tags: list[str] 

class BaseResponseProject(BaseModel):
    id: UUID
    name: str = Field(title="Название проекта", examples=["ХаляваОнлайн"])
    description: str | None = None
    status: str

class DetailedResponseProject(BaseResponseProject):
    start_at: date
    end_at: date
    total_required_investment: Decimal
    remaining_required_investment: Decimal
    min_investment: Decimal
    tags: list[str] 