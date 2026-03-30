from datetime import datetime

from pydantic import BaseModel, Field

from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int = Field(..., ge=1)
    quantity: int = Field(..., ge=1)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    amount: float


class OrderRead(BaseModel):
    id: int
    buyer_id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemRead]


class OrderListData(BaseModel):
    items: list[OrderRead]
