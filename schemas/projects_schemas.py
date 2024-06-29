from datetime import date
from pydantic import BaseModel, Field

class ShowProject(BaseModel):
    name: str = Field(title="Название проекта", examples=["ХаляваОнлайн"])
    description: str | None = None
    start_at: date
    end_at: date
    total_required_investmenet: int
    remaining_required_investment: int
    tags: list[str]

class CreateProject(ShowProject):
    pass