from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.order import Order
    from app.models.product import Product


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
