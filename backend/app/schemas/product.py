from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import PaginationMeta


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(..., gt=0)
    unit: str = Field(..., min_length=1, max_length=30)
    stock: int = Field(..., ge=0)
    image_url: str | None = None
    category_id: int = Field(..., ge=1)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    unit: str | None = Field(default=None, min_length=1, max_length=30)
    stock: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    category_id: int | None = Field(default=None, ge=1)


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    unit: str
    stock: int
    image_url: str | None
    seller_id: int
    category_id: int
    created_at: datetime
    seller_name: str
    category_name: str

    model_config = {"from_attributes": True}


class ProductListData(BaseModel):
    items: list[ProductRead]
    pagination: PaginationMeta
