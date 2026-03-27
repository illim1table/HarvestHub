from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    id: int
    name: str
    category: str
    price: float
    unit: str
    stock: int
    description: Optional[str] = None
    seller: str
    image_url: Optional[str] = None
