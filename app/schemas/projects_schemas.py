from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

class ShowProject(BaseModel):
    name: str = Field(title="Название проекта", examples=["ХаляваОнлайн"])
    description: str | None = None
    start_at: date
    end_at: date
    total_required_investmenet: Decimal
    remaining_required_investment: Decimal
    min_investment: Decimal
    tags: list[str] 

class CreateProject(ShowProject):
    pass