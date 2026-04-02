from datetime import datetime
from enum import Enum

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
    payment_trade_no: str | None = None
    paid_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemRead]


class OrderListData(BaseModel):
    items: list[OrderRead]


class PayStatus(str, Enum):
    success = "success"
    failed = "failed"


class MockPaymentRequest(BaseModel):
    order_id: int = Field(..., ge=1)
    trade_no: str = Field(..., min_length=1, max_length=64)
    pay_status: PayStatus


class SellerOrderListData(BaseModel):
    items: list[OrderRead]
