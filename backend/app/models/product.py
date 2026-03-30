from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.order_item import OrderItem
    from app.models.user import User


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    seller: Mapped["User"] = relationship("User", back_populates="products")
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")
