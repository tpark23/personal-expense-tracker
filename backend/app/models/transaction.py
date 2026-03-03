from typing import Optional
from pydantic import BaseModel


class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    category: Optional[str] = None